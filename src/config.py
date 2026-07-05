"""
Backend configuration — settings, env vars, constants.
Uses pydantic-settings for type-safe env loading.
"""

from __future__ import annotations
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5-chat", alias="OPENAI_MODEL")

    # Azure OpenAI
    azure_api_key: str = Field(default="", alias="AZURE_API_KEY")
    azure_api_base: str = Field(default="", alias="AZURE_API_BASE")
    azure_api_version: str = Field(default="", alias="AZURE_API_VERSION")
    azure_deployment: str = Field(default="", alias="AZURE_DEPLOYMENT")

    # App
    backend_url: str = Field(default="http://localhost:8000", alias="BACKEND_URL")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    demo_mode: bool = Field(default=True, alias="DEMO_MODE")

    # Paths
    @property
    def base_dir(self) -> str:
        return os.path.dirname(os.path.dirname(__file__))

    @property
    def generated_dir(self) -> str:
        return os.path.join(self.base_dir, "generated")

    @property
    def prompt_trace_dir(self) -> str:
        return os.path.join(self.base_dir, "prompt_trace")

    @property
    def sample_data_dir(self) -> str:
        return os.path.join(self.base_dir, "sample_data")

    @property
    def has_api_key(self) -> bool:
        # Standard OpenAI
        if self.openai_api_key and not self.openai_api_key.startswith("sk-..."):
            return True
        # Azure OpenAI — both key and endpoint must be present
        return bool(self.azure_api_key and self.azure_api_base)

    model_config = {"env_file": ".env", "extra": "ignore", "populate_by_name": True}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Ensure directories exist at import time
def _ensure_dirs():
    s = get_settings()
    for d in [s.generated_dir, s.prompt_trace_dir, s.sample_data_dir,
              os.path.join(s.generated_dir, "vendors"),
              os.path.join(s.generated_dir, "extractions")]:
        os.makedirs(d, exist_ok=True)


_ensure_dirs()

