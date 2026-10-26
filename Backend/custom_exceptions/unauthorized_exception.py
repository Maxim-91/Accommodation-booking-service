class UnauthorizedException(Exception):
    def __init__(
        self,
        message: str = "Invalid email or password",
    ) -> None:
        super().__init__(message)
        