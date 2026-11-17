import unittest
from unittest.mock import Mock
from passlib.hash import argon2
from tests.unit.test_helpers import create_test_session
from services.user_service import UserService
from tools.abc_token_tool import ABCTokenTool
from models import User
from custom_exceptions.conflict_exception import ConflictException
from custom_exceptions.unauthorized_exception import UnauthorizedException
import jwt


class UserServiceTests(unittest.TestCase):

    def setUp(self):
        self.engine, self.session = create_test_session()
        self.token_tool = Mock(spec=ABCTokenTool)
        self.service = UserService(self.session, self.token_tool)

    # def tearDown for close and destroy the engine
    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    # Check registration
    def test_register_creates_user_with_hashed_password(self):
        user = self.service.register(full_name="Test User", email="TEST@example.com", password="password123")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.full_name, "Test User")
        self.assertNotEqual(user.password_hash, "password123")
        self.assertTrue(argon2.verify("password123", user.password_hash))

    # Check re-registration
    def test_register_duplicate_email_raises_conflict(self):
        self.service.register(full_name="First User", email="test@example.com", password="password123")

        with self.assertRaises(ConflictException):
            self.service.register(full_name="Second User", email="TEST@example.com", password="password456")

    # Check login
    def test_login_returns_access_token(self):
        self.service.register(full_name="Test User", email="test@example.com", password="password123")
        self.token_tool.create_token.return_value = "fake-access-token"
        token = self.service.login(email="TEST@example.com", password="password123")
        self.assertEqual(token, "fake-access-token")
        self.token_tool.create_token.assert_called_once()

    # Check incorrect password
    def test_login_with_wrong_password_raises_unauthorized(self):
        self.service.register(full_name="Test User", email="test@example.com", password="password123")

        with self.assertRaises(UnauthorizedException):
            self.service.login(email="test@example.com", password="wrong-password")

    # Check a non-existent user
    def test_login_unknown_email_raises_unauthorized(self):
        with self.assertRaises(UnauthorizedException):
            self.service.login(email="unknown@example.com", password="password123")

    # Check token decoding: valid and invalid
    def test_get_user_by_valid_access_token(self):
        user = self.service.register(full_name="Test User", email="test@example.com", password="password123")
        self.token_tool.decode_token.return_value = { "sub": str(user.id) }
        result = self.service.get_user_by_access_token("valid-token")
        self.assertEqual(result.id, user.id)

    def test_get_user_by_invalid_access_token_returns_none(self):
        self.token_tool.decode_token.side_effect = jwt.InvalidTokenError("Invalid token")
        result = self.service.get_user_by_access_token("invalid-token")
        self.assertIsNone(result)
