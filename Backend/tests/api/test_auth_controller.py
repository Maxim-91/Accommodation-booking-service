import unittest
from unittest.mock import Mock
from tests.api.test_helpers import ApiTestCaseMixin, app
from factories.services import token_tool_factory
from tools.abc_token_tool import ABCTokenTool


class AuthControllerApiTests(ApiTestCaseMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.token_tool = Mock(spec=ABCTokenTool)
        self.token_tool.create_token.return_value = "test-access-token"
        app.dependency_overrides[token_tool_factory] = lambda: self.token_tool

    def test_register_user_returns_created_user(self):
        response = self.client.post(
            "/api/auth/register",
            json={
                "full_name": "API Test User",
                "email": "api-user@example.com",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["full_name"], "API Test User")
        self.assertEqual(body["email"], "api-user@example.com")
        self.assertIn("id", body)
        self.assertNotIn("password_hash", body)

    def test_register_duplicate_email_returns_conflict(self):
        payload = {
            "full_name": "API Test User",
            "email": "duplicate@example.com",
            "password": "password123",
        }
        self.assertEqual(self.client.post("/api/auth/register", json=payload).status_code, 201)
        response = self.client.post(
            "/api/auth/register",
            json={**payload, "full_name": "Second User"},
        )
        self.assertEqual(response.status_code, 409)

    def test_register_invalid_payload_returns_validation_error(self):
        response = self.client.post(
            "/api/auth/register",
            json={"full_name": "", "email": "not-an-email", "password": "short"},
        )
        self.assertEqual(response.status_code, 422)

    def test_login_returns_bearer_access_token(self):
        self.client.post(
            "/api/auth/register",
            json={
                "full_name": "Login User",
                "email": "login@example.com",
                "password": "password123",
            },
        )
        response = self.client.post(
            "/api/auth/login",
            json={"email": "LOGIN@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"access_token": "test-access-token", "token_type": "bearer"},
        )
        self.token_tool.create_token.assert_called_once()

    def test_login_with_wrong_password_returns_unauthorized(self):
        self.client.post(
            "/api/auth/register",
            json={
                "full_name": "Login User",
                "email": "login-wrong@example.com",
                "password": "password123",
            },
        )
        response = self.client.post(
            "/api/auth/login",
            json={"email": "login-wrong@example.com", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["title"], "unauthorized")


if __name__ == "__main__":
    unittest.main()
