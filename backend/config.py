from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    # Have to specify python, where to read the .env variables from. In this case it is .env file.
    # This is specified using the SettingsConfigDict given by the pydantic_settings module.
    # As the name suggests (model_config) where the model fetches it's values from, that is, the data about the model which is specified using the SettingsConfigDict().
    model_config = SettingsConfigDict(
        env_file="backend/.env",
        extra="ignore"
    )

# Defining the Settings class that can be imported in any file to access the .env variables using this Class.
Config = Settings()