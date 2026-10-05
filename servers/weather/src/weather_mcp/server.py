import asyncio
import os

from functools import lru_cache

from mcp.server.mcpserver import MCPServer
from webclients.services.geocoding import GeocodingService
from webclients.services.openweather import OpenWeatherService

from .schemas import Location, LocationResolutionResult
from .schemas import WeatherResult
from .config import Settings


server = MCPServer("weather MCP")

geocoding_service = GeocodingService()

@lru_cache
def get_weather_service() -> OpenWeatherService:
    settings = Settings.from_environment()
    return OpenWeatherService(api_key=settings.openweather_api_key)





@server.tool()
def geocode_location(query: str) -> LocationResolutionResult:
    """
    Resolve  a human-readable location name to its geographical coordinates.

    Args:
        query (str): The query for the location to resolve.

    Returns:
        LocationResolutionResult: The result of the location resolution.
    """


    ## Removed limit as a parameter for MCP capability to keep it simpler for agents. The limit is now hardcoded to 5 results.
    results = geocoding_service.geocode(query, limit=5)

    resolved_locations = [
        Location(
            name=result.name,
            latitude=result.latitude,
            longitude=result.longitude,
            address=result.address
        )
        for result in results
    ]


    if not resolved_locations or len(resolved_locations) == 0:
        status = "not_found"
    elif len(resolved_locations) == 1:
        status = "resolved"
    else:
        status = "ambiguous"


    return LocationResolutionResult(status=status, locations=resolved_locations)
    
@server.tool()
def get_weather(latitude: float, longitude: float) -> WeatherResult:
    """
    Get the weather for a given location.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        """

    result = get_weather_service().fetch_current_weather(lat=latitude, lon=longitude)
    # For demonstration purposes, we'll return a mock weather response.
    # In a real implementation, you would fetch data from a weather API.

    return WeatherResult(
        city=result["city_name"],
        temperature=result["temp_celsius"],
        summary=result["summary"],
        humidity=result["humidity"]
    )

async def main() -> None:
    await server.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
