from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    jwt_secret: str
    jwt_expiry_seconds: int = 3600

    @staticmethod
    def default() -> "AppConfig":
        return AppConfig(jwt_secret="dev-secret", jwt_expiry_seconds=3600)
