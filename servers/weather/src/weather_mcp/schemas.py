from typing import Literal

from pydantic import BaseModel, Field

class Location(BaseModel):
    name : str = Field(..., description="Name of the location")
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    address: str = Field(..., description="Address of the location")


class LocationResolutionResult(BaseModel):
    status: Literal["resolved", "ambiguous","not_found"] = Field(..., description="Status of the location resolution")
    locations: list[Location] = Field(default_factory=list, description="List of resolved locations")


class WeatherResult(BaseModel):
    city: str = Field(..., description="Name of the city")
    temperature: float = Field(..., description="Temperature in Celsius")
    summary: str = Field(..., description="Weather condition (e.g., sunny, cloudy, rainy)")
    humidity: float = Field(..., description="Humidity percentage")