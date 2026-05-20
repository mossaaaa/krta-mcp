#!/usr/bin/env python3
"""
Karta Markets MCP Server

A Model Context Protocol server for tracking meme coins on the Solana blockchain
using the Karta Markets platform. Provides tools for monitoring market capitalization,
trading volume, price movements, and other key metrics for Solana-based meme coins.

Author: Generated for Karta Markets Integration
License: MIT
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json
import os
import httpx

# Initialize the MCP server (host/port used for SSE and streamable-http)
mcp = FastMCP(
    "karta_markets_mcp",
    host=os.environ.get("FASTMCP_HOST", "127.0.0.1"),
    port=int(os.environ.get("FASTMCP_PORT", "8000")),
    sse_path=os.environ.get("FASTMCP_SSE_PATH", "/sse"),
    streamable_http_path=os.environ.get("FASTMCP_STREAMABLE_HTTP_PATH", "/mcp"),
)

# Constants
KARTA_API_BASE_URL = "https://karta.markets"  # Placeholder - adjust based on actual API
DEFAULT_TIMEOUT = 30.0
MAX_RESULTS = 100

# ============================================================================
# Enums and Type Definitions
# ============================================================================

class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class TimeFrame(str, Enum):
    """Time frame options for historical data."""
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    HOUR_24 = "24h"
    DAYS_7 = "7d"
    DAYS_30 = "30d"


class SortBy(str, Enum):
    """Sorting options for coin listings."""
    MARKET_CAP = "market_cap"
    VOLUME = "volume"
    PRICE = "price"
    PRICE_CHANGE = "price_change"
    HOLDERS = "holders"
    AGE = "age"


class SortOrder(str, Enum):
    """Sort order direction."""
    ASC = "asc"
    DESC = "desc"


# ============================================================================
# Pydantic Models for Input Validation
# ============================================================================

class SearchCoinsInput(BaseModel):
    """Input model for searching Solana meme coins."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    query: Optional[str] = Field(
        default=None,
        description="Search query for coin name, symbol, or contract address",
        max_length=200
    )
    min_market_cap: Optional[float] = Field(
        default=None,
        description="Minimum market capitalization in USD (e.g., 100000 for $100k)",
        ge=0
    )
    max_market_cap: Optional[float] = Field(
        default=None,
        description="Maximum market capitalization in USD",
        ge=0
    )
    min_volume_24h: Optional[float] = Field(
        default=None,
        description="Minimum 24-hour trading volume in USD",
        ge=0
    )
    max_volume_24h: Optional[float] = Field(
        default=None,
        description="Maximum 24-hour trading volume in USD",
        ge=0
    )
    min_holders: Optional[int] = Field(
        default=None,
        description="Minimum number of token holders",
        ge=0
    )
    sort_by: SortBy = Field(
        default=SortBy.MARKET_CAP,
        description="Field to sort results by"
    )
    sort_order: SortOrder = Field(
        default=SortOrder.DESC,
        description="Sort order direction (ascending or descending)"
    )
    limit: int = Field(
        default=20,
        description="Maximum number of results to return",
        ge=1,
        le=MAX_RESULTS
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )

    @field_validator('max_market_cap')
    @classmethod
    def validate_market_cap_range(cls, v: Optional[float], info) -> Optional[float]:
        """Ensure max_market_cap is greater than min_market_cap if both are set."""
        if v is not None and info.data.get('min_market_cap') is not None:
            if v <= info.data['min_market_cap']:
                raise ValueError("max_market_cap must be greater than min_market_cap")
        return v


class GetCoinDetailsInput(BaseModel):
    """Input model for retrieving detailed coin information."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    coin_id: str = Field(
        ...,
        description="Coin identifier (contract address, symbol, or Karta Markets ID)",
        min_length=1,
        max_length=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class GetPriceHistoryInput(BaseModel):
    """Input model for retrieving price history."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    coin_id: str = Field(
        ...,
        description="Coin identifier (contract address, symbol, or Karta Markets ID)",
        min_length=1,
        max_length=100
    )
    time_frame: TimeFrame = Field(
        default=TimeFrame.HOUR_24,
        description="Time frame for historical data"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class GetTrendingCoinsInput(BaseModel):
    """Input model for retrieving trending meme coins."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    limit: int = Field(
        default=10,
        description="Maximum number of trending coins to return",
        ge=1,
        le=50
    )
    time_frame: TimeFrame = Field(
        default=TimeFrame.HOUR_24,
        description="Time frame for trending calculation"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class GetMarketOverviewInput(BaseModel):
    """Input model for retrieving market overview statistics."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


# ============================================================================
# Helper Functions
# ============================================================================

async def make_api_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET"
) -> Dict[str, Any]:
    """
    Make an API request to Karta Markets.
    
    Args:
        endpoint: API endpoint path
        params: Query parameters
        method: HTTP method
        
    Returns:
        API response as dictionary
        
    Raises:
        httpx.HTTPStatusError: If the request fails
    """
    url = f"{KARTA_API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return _handle_api_error(e)


def _handle_api_error(e: Exception) -> Dict[str, Any]:
    """
    Format API errors consistently.
    
    Args:
        e: Exception that occurred
        
    Returns:
        Error information dictionary
    """
    if isinstance(e, httpx.HTTPStatusError):
        status_code = e.response.status_code
        if status_code == 404:
            return {"error": "Resource not found. Please check the coin ID or parameters."}
        elif status_code == 403:
            return {"error": "Access denied. Please check your API credentials."}
        elif status_code == 429:
            return {"error": "Rate limit exceeded. Please wait before making more requests."}
        elif status_code >= 500:
            return {"error": f"Server error (status {status_code}). Please try again later."}
        return {"error": f"API request failed with status {status_code}"}
    elif isinstance(e, httpx.TimeoutException):
        return {"error": "Request timed out. Please try again."}
    return {"error": f"Unexpected error: {type(e).__name__}"}


def format_currency(value: float, decimals: int = 2) -> str:
    """Format a number as USD currency."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.{decimals}f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.{decimals}f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.{decimals}f}K"
    else:
        return f"${value:.{decimals}f}"


def format_percentage(value: float) -> str:
    """Format a number as a percentage with appropriate sign."""
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def format_large_number(value: int) -> str:
    """Format large numbers with appropriate suffix."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)


def format_coin_data_markdown(coin: Dict[str, Any]) -> str:
    """
    Format coin data as markdown.
    
    Args:
        coin: Coin data dictionary
        
    Returns:
        Formatted markdown string
    """
    name = coin.get('name', 'Unknown')
    symbol = coin.get('symbol', 'N/A')
    price = coin.get('price', 0)
    market_cap = coin.get('market_cap', 0)
    volume_24h = coin.get('volume_24h', 0)
    price_change_24h = coin.get('price_change_24h', 0)
    holders = coin.get('holders', 0)
    contract_address = coin.get('contract_address', 'N/A')
    
    return f"""### {name} ({symbol})

**Price:** {format_currency(price, 6)}
**Market Cap:** {format_currency(market_cap)}
**24h Volume:** {format_currency(volume_24h)}
**24h Change:** {format_percentage(price_change_24h)}
**Holders:** {format_large_number(holders)}
**Contract Address:** `{contract_address}`
"""


def format_coins_list_markdown(coins: List[Dict[str, Any]], title: str = "Results") -> str:
    """
    Format a list of coins as markdown.
    
    Args:
        coins: List of coin data dictionaries
        title: Title for the results section
        
    Returns:
        Formatted markdown string
    """
    if not coins:
        return "No coins found matching the criteria."
    
    output = f"## {title}\n\nFound {len(coins)} coin(s):\n\n"
    
    for i, coin in enumerate(coins, 1):
        name = coin.get('name', 'Unknown')
        symbol = coin.get('symbol', 'N/A')
        price = coin.get('price', 0)
        market_cap = coin.get('market_cap', 0)
        volume_24h = coin.get('volume_24h', 0)
        price_change_24h = coin.get('price_change_24h', 0)
        
        output += f"{i}. **{name} ({symbol})**\n"
        output += f"   - Price: {format_currency(price, 6)}\n"
        output += f"   - Market Cap: {format_currency(market_cap)}\n"
        output += f"   - 24h Volume: {format_currency(volume_24h)}\n"
        output += f"   - 24h Change: {format_percentage(price_change_24h)}\n\n"
    
    return output


def format_market_overview_markdown(overview: Dict[str, Any]) -> str:
    """
    Format market overview data as markdown.
    
    Args:
        overview: Market overview data dictionary
        
    Returns:
        Formatted markdown string
    """
    total_market_cap = overview.get('total_market_cap', 0)
    total_volume_24h = overview.get('total_volume_24h', 0)
    total_coins = overview.get('total_coins', 0)
    trending_count = overview.get('trending_count', 0)
    
    return f"""## Solana Meme Coin Market Overview

**Total Market Cap:** {format_currency(total_market_cap)}
**24h Trading Volume:** {format_currency(total_volume_24h)}
**Total Tracked Coins:** {format_large_number(total_coins)}
**Trending Coins (24h):** {trending_count}

*Data provided by Karta Markets*
"""


# ============================================================================
# Mock Data Generators (for demonstration when API is unavailable)
# ============================================================================

def generate_mock_coin_data(coin_id: str) -> Dict[str, Any]:
    """Generate mock coin data for demonstration purposes."""
    import random
    
    return {
        "id": coin_id,
        "name": f"Meme Coin {coin_id[:6]}",
        "symbol": coin_id[:4].upper(),
        "price": random.uniform(0.000001, 1.0),
        "market_cap": random.uniform(100000, 10000000),
        "volume_24h": random.uniform(10000, 1000000),
        "price_change_24h": random.uniform(-50, 100),
        "price_change_7d": random.uniform(-70, 200),
        "holders": random.randint(100, 50000),
        "contract_address": coin_id,
        "liquidity": random.uniform(50000, 500000),
        "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
    }


def generate_mock_coins_list(count: int) -> List[Dict[str, Any]]:
    """Generate a list of mock coins for demonstration."""
    return [generate_mock_coin_data(f"mock_{i}") for i in range(count)]


def generate_mock_price_history(time_frame: str) -> List[Dict[str, Any]]:
    """Generate mock price history data."""
    import random
    
    if time_frame == "1h":
        intervals = 12
        interval_minutes = 5
    elif time_frame == "4h":
        intervals = 16
        interval_minutes = 15
    elif time_frame == "24h":
        intervals = 24
        interval_minutes = 60
    elif time_frame == "7d":
        intervals = 168
        interval_minutes = 60
    else:  # 30d
        intervals = 720
        interval_minutes = 60
    
    history = []
    base_price = random.uniform(0.0001, 0.1)
    current_time = datetime.now()
    
    for i in range(intervals):
        timestamp = current_time - timedelta(minutes=interval_minutes * (intervals - i))
        price = base_price * (1 + random.uniform(-0.1, 0.1))
        volume = random.uniform(10000, 100000)
        
        history.append({
            "timestamp": timestamp.isoformat(),
            "price": price,
            "volume": volume
        })
    
    return history


def generate_mock_market_overview() -> Dict[str, Any]:
    """Generate mock market overview data."""
    import random
    
    return {
        "total_market_cap": random.uniform(1000000000, 10000000000),
        "total_volume_24h": random.uniform(100000000, 1000000000),
        "total_coins": random.randint(500, 5000),
        "trending_count": random.randint(10, 50),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool(
    name="karta_search_coins",
    annotations={
        "title": "Search Solana Meme Coins",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def search_coins(params: SearchCoinsInput) -> str:
    """Search and filter Solana meme coins on Karta Markets.

    This tool allows you to search for meme coins on the Solana blockchain with
    customizable filters for market capitalization, trading volume, and other metrics.
    You can adjust the market cap range, volume thresholds, and sorting preferences to
    find coins that match your specific criteria.

    Args:
        params (SearchCoinsInput): Search parameters containing:
            - query (Optional[str]): Search query for name, symbol, or address
            - min_market_cap (Optional[float]): Minimum market cap in USD
            - max_market_cap (Optional[float]): Maximum market cap in USD
            - min_volume_24h (Optional[float]): Minimum 24h volume in USD
            - max_volume_24h (Optional[float]): Maximum 24h volume in USD
            - min_holders (Optional[int]): Minimum number of holders
            - sort_by (SortBy): Field to sort by (default: market_cap)
            - sort_order (SortOrder): Sort direction (default: desc)
            - limit (int): Max results to return (default: 20, max: 100)
            - response_format (ResponseFormat): Output format

    Returns:
        str: Formatted list of coins matching the search criteria. In markdown format,
             includes coin name, symbol, price, market cap, 24h volume, and price change.
             In JSON format, returns complete structured data with all available fields.

    Examples:
        - Search for coins with market cap between $100K and $1M
        - Find coins with high 24h volume (>$50K)
        - Sort by price change to find biggest gainers
        - Filter by minimum holder count
    """
    try:
        # In production, this would make an actual API call
        # For now, using mock data for demonstration
        
        # Build query parameters
        api_params = {}
        if params.query:
            api_params['search'] = params.query
        if params.min_market_cap:
            api_params['min_market_cap'] = params.min_market_cap
        if params.max_market_cap:
            api_params['max_market_cap'] = params.max_market_cap
        if params.min_volume_24h:
            api_params['min_volume'] = params.min_volume_24h
        if params.max_volume_24h:
            api_params['max_volume'] = params.max_volume_24h
        if params.min_holders:
            api_params['min_holders'] = params.min_holders
        
        api_params['sort_by'] = params.sort_by.value
        api_params['sort_order'] = params.sort_order.value
        api_params['limit'] = params.limit
        
        # Mock API call - replace with actual API integration
        coins = generate_mock_coins_list(params.limit)
        
        # Apply filters to mock data
        if params.min_market_cap:
            coins = [c for c in coins if c['market_cap'] >= params.min_market_cap]
        if params.max_market_cap:
            coins = [c for c in coins if c['market_cap'] <= params.max_market_cap]
        if params.min_volume_24h:
            coins = [c for c in coins if c['volume_24h'] >= params.min_volume_24h]
        if params.max_volume_24h:
            coins = [c for c in coins if c['volume_24h'] <= params.max_volume_24h]
        if params.min_holders:
            coins = [c for c in coins if c['holders'] >= params.min_holders]
        
        # Sort results
        reverse = params.sort_order == SortOrder.DESC
        coins.sort(key=lambda x: x.get(params.sort_by.value, 0), reverse=reverse)
        
        # Format response
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                "total": len(coins),
                "filters": api_params,
                "coins": coins
            }, indent=2)
        else:
            return format_coins_list_markdown(coins, "Search Results")
            
    except Exception as e:
        error_info = _handle_api_error(e)
        return json.dumps(error_info, indent=2) if params.response_format == ResponseFormat.JSON else f"Error: {error_info.get('error', str(e))}"


@mcp.tool(
    name="karta_get_coin_details",
    annotations={
        "title": "Get Detailed Coin Information",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_coin_details(params: GetCoinDetailsInput) -> str:
    """Retrieve comprehensive details for a specific Solana meme coin.

    Get in-depth information about a meme coin including current price, market
    capitalization, trading volume, holder statistics, contract details, and
    historical performance metrics. This tool provides all available data for
    a single coin to support detailed analysis.

    Args:
        params (GetCoinDetailsInput): Parameters containing:
            - coin_id (str): Coin identifier (contract address, symbol, or ID)
            - response_format (ResponseFormat): Output format

    Returns:
        str: Detailed coin information. In markdown format, presents data in a
             structured, readable layout with formatted numbers and percentages.
             In JSON format, returns complete raw data with all available fields
             including metadata, liquidity info, and creation timestamp.

    Examples:
        - Get details for a coin by contract address
        - Look up coin information by symbol
        - Retrieve full metrics for portfolio tracking
    """
    try:
        # Mock API call - replace with actual implementation
        coin_data = generate_mock_coin_data(params.coin_id)
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(coin_data, indent=2)
        else:
            return format_coin_data_markdown(coin_data)
            
    except Exception as e:
        error_info = _handle_api_error(e)
        return json.dumps(error_info, indent=2) if params.response_format == ResponseFormat.JSON else f"Error: {error_info.get('error', str(e))}"


@mcp.tool(
    name="karta_get_price_history",
    annotations={
        "title": "Get Price History",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_price_history(params: GetPriceHistoryInput) -> str:
    """Retrieve historical price and volume data for a meme coin.

    Access time-series data showing how a coin's price and trading volume have
    changed over different time periods. Useful for trend analysis, identifying
    patterns, and making informed trading decisions based on historical performance.

    Args:
        params (GetPriceHistoryInput): Parameters containing:
            - coin_id (str): Coin identifier
            - time_frame (TimeFrame): Period to retrieve (1h, 4h, 24h, 7d, 30d)
            - response_format (ResponseFormat): Output format

    Returns:
        str: Historical price data. In markdown format, shows a summary with
             high/low prices, volume statistics, and key data points. In JSON
             format, returns complete time-series array with timestamp, price,
             and volume for each interval.

    Examples:
        - View 24-hour price chart data
        - Analyze 7-day trading patterns
        - Track 30-day performance trends
    """
    try:
        # Mock API call - replace with actual implementation
        history = generate_mock_price_history(params.time_frame.value)
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                "coin_id": params.coin_id,
                "time_frame": params.time_frame.value,
                "data_points": len(history),
                "history": history
            }, indent=2)
        else:
            # Calculate statistics
            prices = [h['price'] for h in history]
            volumes = [h['volume'] for h in history]
            
            high = max(prices)
            low = min(prices)
            avg_volume = sum(volumes) / len(volumes)
            
            output = f"""## Price History for {params.coin_id}

**Time Frame:** {params.time_frame.value}
**Data Points:** {len(history)}

**Price Statistics:**
- High: {format_currency(high, 6)}
- Low: {format_currency(low, 6)}
- Current: {format_currency(prices[-1], 6)}

**Volume Statistics:**
- Average Volume: {format_currency(avg_volume)}
- Latest Volume: {format_currency(volumes[-1])}

*Use JSON format for complete time-series data*
"""
            return output
            
    except Exception as e:
        error_info = _handle_api_error(e)
        return json.dumps(error_info, indent=2) if params.response_format == ResponseFormat.JSON else f"Error: {error_info.get('error', str(e))}"


@mcp.tool(
    name="karta_get_trending",
    annotations={
        "title": "Get Trending Meme Coins",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_trending_coins(params: GetTrendingCoinsInput) -> str:
    """Discover currently trending Solana meme coins.

    Identify meme coins that are experiencing significant price movement, volume
    increases, or social activity. Trending coins are ranked based on multiple
    factors including price change, volume growth, and holder activity over the
    specified time frame.

    Args:
        params (GetTrendingCoinsInput): Parameters containing:
            - limit (int): Max number of trending coins (default: 10, max: 50)
            - time_frame (TimeFrame): Period for trending calculation
            - response_format (ResponseFormat): Output format

    Returns:
        str: List of trending coins ranked by momentum. Includes current price,
             price change percentage, volume metrics, and ranking position.

    Examples:
        - Find top 10 trending coins in the last 24 hours
        - Discover coins with strongest momentum this week
        - Track emerging meme coin trends
    """
    try:
        # Mock API call - replace with actual implementation
        coins = generate_mock_coins_list(params.limit)
        
        # Sort by price change (trending metric)
        coins.sort(key=lambda x: x['price_change_24h'], reverse=True)
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                "time_frame": params.time_frame.value,
                "trending_count": len(coins),
                "coins": coins
            }, indent=2)
        else:
            return format_coins_list_markdown(coins, f"Trending Coins ({params.time_frame.value})")
            
    except Exception as e:
        error_info = _handle_api_error(e)
        return json.dumps(error_info, indent=2) if params.response_format == ResponseFormat.JSON else f"Error: {error_info.get('error', str(e))}"


@mcp.tool(
    name="karta_get_market_overview",
    annotations={
        "title": "Get Market Overview",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_market_overview(params: GetMarketOverviewInput) -> str:
    """Get overall statistics for the Solana meme coin market.

    Retrieve aggregated metrics providing a high-level view of the entire Solana
    meme coin ecosystem. Includes total market capitalization, trading volume,
    number of tracked coins, and other market-wide statistics.

    Args:
        params (GetMarketOverviewInput): Parameters containing:
            - response_format (ResponseFormat): Output format

    Returns:
        str: Market overview statistics including total market cap, 24h volume,
             number of coins tracked, and trending coin count.

    Examples:
        - Check overall market health
        - Monitor total ecosystem size
        - Track market-wide trends
    """
    try:
        # Mock API call - replace with actual implementation
        overview = generate_mock_market_overview()
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(overview, indent=2)
        else:
            return format_market_overview_markdown(overview)
            
    except Exception as e:
        error_info = _handle_api_error(e)
        return json.dumps(error_info, indent=2) if params.response_format == ResponseFormat.JSON else f"Error: {error_info.get('error', str(e))}"


# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Karta Markets MCP Server — stdio, SSE, or streamable HTTP"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport: stdio (default), sse, or streamable-http",
    )
    parser.add_argument(
        "--mount-path",
        default=None,
        help="Mount path for SSE (default: /). Ignored for stdio/streamable-http.",
    )
    parser.add_argument("--host", default=None, help="Host for SSE/streamable-http (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=None, help="Port for SSE/streamable-http (default: 8000)")
    args = parser.parse_args()

    if args.host is not None:
        mcp.settings.host = args.host
    if args.port is not None:
        mcp.settings.port = args.port

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        print(f"SSE server: http://{mcp.settings.host}:{mcp.settings.port}{mcp.settings.sse_path}")
        print(f"Messages:   http://{mcp.settings.host}:{mcp.settings.port}{mcp.settings.message_path}")
        mcp.run(transport="sse", mount_path=args.mount_path)
    else:
        print(f"Streamable HTTP: http://{mcp.settings.host}:{mcp.settings.port}{mcp.settings.streamable_http_path}")
        mcp.run(transport="streamable-http")
