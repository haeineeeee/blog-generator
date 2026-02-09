from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-5-20250929"
    wordpress_url: str = ""
    wordpress_username: str = ""
    wordpress_app_password: str = ""
    output_dir: str = "./output"

    model_config = {"env_file": ".env"}


settings = Settings()
