import os

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    json_file: str = Field(..., env='TAFELBERG_API_JSON_FILE')