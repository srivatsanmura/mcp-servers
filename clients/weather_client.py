import asyncio

import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:


    server_params = StdioServerParameters(
        command = "uv",
        args = [
            "run",
            "--package",
            "weather-mcp",
            "python",
            "-m",
            "weather_mcp.server",
        ],
        env = os.environ.copy(),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("Discovered tools:" )
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            

            result = await session.call_tool(
                "geocode_location",
                arguments={"query": "Chennai"},
            )

            print("Geocode result for 'Chennai':")
            print(result)

            if result.is_error:
                raise RuntimeError(f"Error calling geocode_location: {result.error_message}")

            location = result.structured_content["locations"][0]

            weather_result = await session.call_tool(
                "get_weather",
                arguments={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                },
            )

            print("Weather result:")
            print(weather_result)

if __name__ == "__main__":
    asyncio.run(main())