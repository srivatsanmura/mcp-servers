from unittest.mock import Mock

from types import SimpleNamespace
from weather_mcp.server import geocode_location, get_weather


def test_geocode_location_resolved(monkeypatch):
    
    mock_result = SimpleNamespace(
        name="Chennai, Tamil Nadu, India",
        latitude=13.0827,
        longitude=80.2707,
        address="Chennai, Tamil Nadu, India",
    )

    mock_service = Mock()
    mock_service.geocode.return_value = [mock_result]

    monkeypatch.setattr(
        "weather_mcp.server.geocoding_service",
        mock_service,
    )

    result = geocode_location("Chennai")

    assert result.status == "resolved"
    assert len(result.locations) == 1
    assert result.locations[0].name == "Chennai, Tamil Nadu, India"
    assert result.locations[0].latitude == 13.0827
    assert result.locations[0].longitude == 80.2707
    assert result.locations[0].address == "Chennai, Tamil Nadu, India"

    mock_service.geocode.assert_called_once_with("Chennai", limit=5)


def test_geocode_location_ambiguous(monkeypatch):
    mock_results = [
        SimpleNamespace(
        name="Springfield, Illinois, USA",
        latitude=39.7817,
        longitude=-89.6501,
        address="Springfield, Illinois, USA",
    ), SimpleNamespace(
        name="Springfield, Massachusetts, USA",
        latitude=42.1015,
        longitude=-72.5898,
        address="Springfield, Massachusetts, USA",
    )
    ]

    mock_service = Mock()
    mock_service.geocode.return_value = mock_results

    monkeypatch.setattr(
        "weather_mcp.server.geocoding_service",
        mock_service,
    )

    result = geocode_location("Springfield")

    assert result.status == "ambiguous"
    assert len(result.locations) == 2
    assert result.locations[0].name == "Springfield, Illinois, USA"
    assert result.locations[1].name == "Springfield, Massachusetts, USA"

def test_geocode_location_not_found(monkeypatch):
    mock_service = Mock()
    mock_service.geocode.return_value = []

    monkeypatch.setattr(
        "weather_mcp.server.geocoding_service",
        mock_service,
    )

    result = geocode_location("Nonexistent Place")

    assert result.status == "not_found"
    assert len(result.locations) == 0

## Now run unittests for fetching weather data for a resolved location

def test_get_weather(monkeypatch):
    mock_service = Mock()
    mock_service.fetch_current_weather.return_value = {
        "city_name": "Chennai",
        "temp_celsius": 30.5,
        "summary": "clear sky",
        "humidity": 70.0,
    }

    monkeypatch.setattr(
        "weather_mcp.server.get_weather_service",
        lambda: mock_service,
    )

    result = get_weather(13.0827, 80.2707)

    assert result.city == "Chennai"
    assert result.temperature == 30.5
    assert result.summary == "clear sky"
    assert result.humidity == 70.0
    
    mock_service.fetch_current_weather.assert_called_once_with(
        lat=13.0827,
        lon=80.2707,
    )
