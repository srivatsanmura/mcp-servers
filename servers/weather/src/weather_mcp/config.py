import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    openweather_api_key: str

    @classmethod
    def from_environment(cls) -> "Settings":
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENWEATHER_API_KEY environment variable is not set.")
        return cls(openweather_api_key=api_key)
