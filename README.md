# Karta Markets MCP Server

A Model Context Protocol (MCP) server for tracking Solana meme coins using the Karta Markets platform. This server provides AI assistants with the ability to search, filter, and analyze meme coins on the Solana blockchain with customizable parameters for market capitalization and trading volume.

## Overview

The Karta Markets MCP Server empowers users by providing real-time data on meme coins within the Solana ecosystem. Users can easily adjust parameters such as market cap and volume to tailor their tracking experience.

### Key Features

- 🔍 **Search & Filter**: Find meme coins by name, symbol, or contract address with customizable filters
- 📊 **Market Cap Tracking**: Monitor coins within specific market capitalization ranges
- 💰 **Volume Analysis**: Filter by 24-hour trading volume to find active coins
- 📈 **Price History**: Access historical price and volume data across multiple timeframes
- 🔥 **Trending Coins**: Discover currently trending meme coins based on momentum
- 📉 **Market Overview**: Get aggregated statistics for the entire Solana meme coin market
- ⚙️ **Editable Parameters**: All filtering parameters (market cap, volume, holders) are fully adjustable
- 🎯 **Multiple Output Formats**: Choose between human-readable Markdown or structured JSON output

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone or download the repository**:
```bash
# If using git
git clone <repository-url>
cd karta-markets-mcp

# Or simply create a directory and download the files
mkdir karta-markets-mcp
cd karta-markets-mcp
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python karta_markets_mcp.py --help
```

## Configuration

### Adding to Claude Desktop

To use this MCP server with Claude Desktop, add the following configuration to your Claude Desktop config file:

**On MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "karta-markets": {
      "command": "python",
      "args": ["/absolute/path/to/karta_markets_mcp.py"]
    }
  }
}
```

Replace `/absolute/path/to/` with the actual path where you saved the `karta_markets_mcp.py` file.

### API Configuration

Currently, this MCP server uses mock data for demonstration purposes. To connect to the actual Karta Markets API:

1. Update the `KARTA_API_BASE_URL` constant in `karta_markets_mcp.py`
2. Add authentication if required (API key, bearer token, etc.)
3. Replace the mock data generators with actual API calls

## Available Tools

### 1. Search Solana Meme Coins (`karta_search_coins`)

Search and filter meme coins with customizable criteria.

**Parameters**:
- `query` (optional): Search by name, symbol, or contract address
- `min_market_cap` (optional): Minimum market cap in USD (e.g., 100000 for $100K)
- `max_market_cap` (optional): Maximum market cap in USD
- `min_volume_24h` (optional): Minimum 24-hour trading volume in USD
- `max_volume_24h` (optional): Maximum 24-hour trading volume in USD
- `min_holders` (optional): Minimum number of token holders
- `sort_by`: Field to sort by (market_cap, volume, price, price_change, holders, age)
- `sort_order`: Sort direction (asc or desc)
- `limit`: Maximum results (1-100, default: 20)
- `response_format`: Output format (markdown or json)

**Example Usage**:
```
Find meme coins with market cap between $100K and $1M, sorted by 24h volume
```

### 2. Get Coin Details (`karta_get_coin_details`)

Retrieve comprehensive information for a specific coin.

**Parameters**:
- `coin_id`: Coin identifier (contract address, symbol, or Karta Markets ID)
- `response_format`: Output format (markdown or json)

**Example Usage**:
```
Get detailed information for coin with address: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

### 3. Get Price History (`karta_get_price_history`)

Access historical price and volume data.

**Parameters**:
- `coin_id`: Coin identifier
- `time_frame`: Period to retrieve (1h, 4h, 24h, 7d, 30d)
- `response_format`: Output format (markdown or json)

**Example Usage**:
```
Show me the 7-day price history for BONK
```

### 4. Get Trending Coins (`karta_get_trending`)

Discover currently trending meme coins.

**Parameters**:
- `limit`: Maximum number of coins (1-50, default: 10)
- `time_frame`: Period for trending calculation (1h, 4h, 24h, 7d, 30d)
- `response_format`: Output format (markdown or json)

**Example Usage**:
```
What are the top 20 trending Solana meme coins in the last 24 hours?
```

### 5. Get Market Overview (`karta_get_market_overview`)

Get aggregated market statistics.

**Parameters**:
- `response_format`: Output format (markdown or json)

**Example Usage**:
```
Give me an overview of the Solana meme coin market
```

## User Guide: Tracking Meme Coins on Solana

### Getting Started

1. **Basic Search**: Simply ask to search for meme coins
   ```
   Search for Solana meme coins
   ```

2. **Filter by Market Cap**: Narrow down results by market capitalization
   ```
   Find meme coins with market cap between $500K and $5M
   ```

3. **Filter by Volume**: Find actively traded coins
   ```
   Show me coins with at least $100K in 24h trading volume
   ```

### Advanced Filtering

You can combine multiple filters to find exactly what you're looking for:

```
Find Solana meme coins with:
- Market cap between $100K and $1M
- At least $50K in 24h volume
- More than 1000 holders
- Sort by price change (biggest gainers first)
```

### Editing Parameters

All parameters are fully editable and can be adjusted at any time:

**Market Cap Range**:
- Set `min_market_cap` to filter out smaller coins
- Set `max_market_cap` to focus on specific size ranges
- Example: `min_market_cap: 100000, max_market_cap: 1000000` for $100K-$1M range

**Volume Filters**:
- Use `min_volume_24h` to find actively traded coins
- Use `max_volume_24h` to exclude highly volatile coins
- Example: `min_volume_24h: 50000` for coins with >$50K daily volume

**Other Filters**:
- `min_holders`: Minimum token holder count
- `sort_by`: Choose ranking metric (market_cap, volume, price, price_change)
- `sort_order`: Ascending or descending order
- `limit`: Control result count (1-100)

### Monitoring Strategies

**For New Opportunities**:
```
Find trending coins with:
- Low market cap ($50K-$500K)
- High volume (>$25K)
- Recent creation (sort by age)
```

**For Established Coins**:
```
Search for coins with:
- Market cap >$1M
- High holder count (>5000)
- Stable volume
```

**For Daily Trading**:
```
Get trending coins:
- Last 24 hours
- Sort by price change
- Minimum volume threshold
```

## Unique Features

### 1. Flexible Parameter System
Unlike fixed tracking tools, all filtering parameters can be adjusted on-the-fly. Simply specify your criteria in natural language, and the MCP server translates them into precise filters.

### 2. Dual Output Formats
- **Markdown**: Human-readable format with formatted numbers, percentages, and organized layout
- **JSON**: Structured data for programmatic processing, integrations, or custom analysis

### 3. Real-Time Filtering
Apply complex, multi-dimensional filters instantly without leaving your AI assistant interface.

### 4. Comprehensive Metrics
Track not just price and market cap, but also:
- Trading volume (24h)
- Price changes (24h and 7d)
- Holder count
- Liquidity data
- Contract addresses
- Creation dates

### 5. Time-Frame Flexibility
Analyze historical data across multiple time frames (1h, 4h, 24h, 7d, 30d) to identify short-term pumps or long-term trends.

## Technical Details

### Architecture

- **Framework**: Built using FastMCP from the official MCP Python SDK
- **Input Validation**: Pydantic v2 models ensure all inputs are validated
- **Error Handling**: Comprehensive error messages guide users toward correct usage
- **Async Support**: All API calls use async/await for optimal performance

### Response Formats

**Markdown Format**:
- Formatted currency values with K/M/B suffixes
- Percentage changes with + or - indicators
- Organized sections with headers and bullet points
- Human-readable timestamps

**JSON Format**:
- Complete structured data
- All available fields included
- Consistent field names
- Suitable for parsing and automation

### Tool Annotations

Each tool includes metadata for optimal AI assistant integration:
- `readOnlyHint`: True (doesn't modify data)
- `destructiveHint`: False (safe to use)
- `idempotentHint`: True (same inputs = same outputs)
- `openWorldHint`: False (doesn't interact with external entities unpredictably)

## Best Practices

### For Investors

1. **Start Broad, Then Narrow**: Begin with a wide search, then refine based on results
2. **Use Multiple Metrics**: Don't rely solely on price—consider volume, holders, and age
3. **Track Trends**: Regular checks for trending coins can identify opportunities early
4. **Set Realistic Filters**: Too narrow filters may return no results

### For Developers

1. **Request JSON Format**: Use `response_format: "json"` for programmatic processing
2. **Implement Pagination**: Use the `limit` parameter to control result size
3. **Cache Results**: Market data changes frequently, but cache can reduce API calls
4. **Error Handling**: Always handle potential errors in responses

### For Traders

1. **Monitor Volume**: High volume often precedes price movements
2. **Check Holder Distribution**: Many holders can indicate healthy distribution
3. **Track Price History**: Use historical data to identify patterns
4. **Set Alerts**: Combine with custom scripts to monitor specific thresholds

## Troubleshooting

### Common Issues

**"No coins found matching criteria"**:
- Your filters may be too restrictive
- Try widening the market cap or volume ranges
- Remove some filters to get broader results

**"Rate limit exceeded"**:
- Wait a few moments before making more requests
- Consider caching frequently accessed data

**"Resource not found"**:
- Verify the coin ID or contract address is correct
- Some coins may not be tracked by Karta Markets

### Getting Help

If you encounter issues:
1. Check the error message for specific guidance
2. Verify your parameter values are within valid ranges
3. Ensure the MCP server is properly configured
4. Review the installation steps

## Development

### Project Structure

```
karta-markets-mcp/
├── karta_markets_mcp.py    # Main MCP server implementation
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── CONFIGURATION_GUIDE.md  # Detailed setup instructions
```

### Extending the Server

To add new tools or modify existing ones:

1. Define a new Pydantic input model
2. Create a tool function with `@mcp.tool()` decorator
3. Implement the tool logic
4. Add proper error handling
5. Update documentation

### Contributing

Contributions are welcome! Please ensure:
- All tools have comprehensive docstrings
- Input validation uses Pydantic models
- Error messages are clear and actionable
- Code follows the existing style

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Data powered by Karta Markets

## Version History

- **v1.0.0** (2026-01-31)
  - Initial release
  - Core search and filtering functionality
  - Support for market cap and volume parameters
  - Price history and trending coins features
  - Comprehensive documentation

---

For more information about Karta Markets, visit [https://karta.markets/](https://karta.markets/)
