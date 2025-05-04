from mcp.server.fastmcp import FastMCP
import calendar_utils

# Create an MCP server
mcp = FastMCP("CalendarServer")

# @mcp.resource("users://{user_id}/profile")
# def get_user_profile(user_id: str) -> str:


@mcp.tool()
def list_events(year: int, month: int) -> str:
    """List calendar events for a given year and month"""
    return "\n".join(calendar_utils.get_calendar_events(year, month))


@mcp.tool()
def add_event(
    summary: str, description: str, start_date: str, end_date: str, timezone: str
) -> str:
    """Add event to calendar, returns html link"""
    return calendar_utils.add_event(
        summary, description, start_date, end_date, timezone
    )


@mcp.tool()
def add_event(summary:str, description:str, start_date:str, end_date:str, timezone:str) -> str:
    """Add event to calendar, returns html link"""

    return calendar_utils.add_event(summary, description, start_date, end_date, timezone)


