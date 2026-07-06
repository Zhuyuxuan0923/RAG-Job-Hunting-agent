from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    tavily_api_key: str = ""
    chroma_persist_dir: str = "./chroma_data"
    model_name: str = "deepseek-v4-pro"
    embedding_api_key: str = ""
    embedding_base_url: str = "https://api.siliconflow.cn/v1"
    embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    embedding_dim: int = 1024

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
