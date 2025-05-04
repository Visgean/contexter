from mcp.server.fastmcp import FastMCP
import calendar_utils
import weather

# Create an MCP server
mcp = FastMCP("CalendarServer")


@mcp.tool()
def list_events(year: int, month: int) -> str:
    """List calendar events for a given year and month"""
    calendar = calendar_utils.Calendar()
    return "\n".join(calendar.get_calendar_events(year, month))


@mcp.tool()
def add_event(
    summary: str, description: str, start_date: str, end_date: str, timezone: str
) -> str:
    """Add event to calendar, returns html link"""
    calendar = calendar_utils.Calendar()

    return calendar.add_event(
        summary, description, start_date, end_date, timezone
    )


@mcp.tool()
def get_weather_forecast(lat, lng) -> str:
    """Add event to calendar, returns html link"""
    return weather.get_weather_forecast(lat, lng)


@mcp.tool()
def get_weather_forecast_prague() -> str:
    """Get weather forecast for Prague, Czech Republic"""
    return weather.get_weather_forecast()
