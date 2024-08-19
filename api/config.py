from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    dbname: str
    user: str
    password: str
    host: str

    class Config:
        env_file = ".env"

# Function to get database settings
def get_db_settings():
    return DatabaseSettings()