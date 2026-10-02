from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str = "http://localhost:8000/auth/callback"
    frontend_url: str = "http://localhost:5173"
    jwt_secret: str
    jwt_expire_hours: int = 24
    first_admin_email: str
    seoul_bus_api_key: str
    gyeonggi_bus_api_key: str
    database_url: str = "sqlite:///./bus_arrival.db"

    class Config:
        env_file = ".env"


settings = Settings()
