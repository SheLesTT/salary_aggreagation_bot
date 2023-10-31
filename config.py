from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host_name:str
    port: int
    user_name: str
    password: str
    bot_token: str

    class Config:
        env_file = ".env"

settings  = Settings()
