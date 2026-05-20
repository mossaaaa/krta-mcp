# Karta Markets MCP Server - Configuration Guide

This guide provides detailed instructions for configuring and deploying the Karta Markets MCP server for tracking Solana meme coins.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration Options](#configuration-options)
4. [Integration with AI Assistants](#integration-with-ai-assistants)
5. [API Configuration](#api-configuration)
6. [Advanced Settings](#advanced-settings)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.10 or higher
- **RAM**: 512 MB minimum (1 GB recommended)
- **Disk Space**: 50 MB for dependencies
- **Network**: Internet connection for API access

### Recommended Setup

- Python 3.11 or 3.12 for optimal performance
- Virtual environment for dependency isolation
- SSD storage for faster data access

## Installation Steps

### Step 1: Install Python

Verify Python is installed and meets version requirements:

```bash
python --version
# or
python3 --version
```

If Python is not installed or version is below 3.10, download from [python.org](https://www.python.org/downloads/).

### Step 2: Create Project Directory

```bash
# Create a dedicated directory
mkdir ~/karta-markets-mcp
cd ~/karta-markets-mcp

# On Windows:
# mkdir %USERPROFILE%\karta-markets-mcp
# cd %USERPROFILE%\karta-markets-mcp
```

### Step 3: Set Up Virtual Environment (Recommended)

Using a virtual environment helps isolate dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
# venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Verify Installation

```bash
# Test the server
python karta_markets_mcp.py --help

# You should see help information about the MCP server
```

## Configuration Options

### Basic Configuration

The MCP server can be configured by editing constants in `karta_markets_mcp.py`:

```python
# API Configuration
KARTA_API_BASE_URL = "https://api.karta.markets"  # Update with actual API URL

# Request Settings
DEFAULT_TIMEOUT = 30.0  # API request timeout in seconds
MAX_RESULTS = 100       # Maximum results per query
```

### Parameter Defaults

You can modify default values for search parameters:

```python
# In SearchCoinsInput model
limit: int = Field(
    default=20,  # Change default result count
    description="Maximum number of results to return",
    ge=1,
    le=MAX_RESULTS
)

sort_by: SortBy = Field(
    default=SortBy.MARKET_CAP,  # Change default sorting
    description="Field to sort results by"
)
```

## Integration with AI Assistants

### Claude Desktop Integration

#### macOS Configuration

1. Locate the config file:
   ```bash
   open ~/Library/Application\ Support/Claude/
   ```

2. Edit `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "karta-markets": {
         "command": "python",
         "args": ["/Users/YOUR_USERNAME/karta-markets-mcp/karta_markets_mcp.py"]
       }
     }
   }
   ```

3. Replace `YOUR_USERNAME` with your actual username

4. If using a virtual environment, use the full path to the Python interpreter:
   ```json
   {
     "mcpServers": {
       "karta-markets": {
         "command": "/Users/YOUR_USERNAME/karta-markets-mcp/venv/bin/python",
         "args": ["/Users/YOUR_USERNAME/karta-markets-mcp/karta_markets_mcp.py"]
       }
     }
   }
   ```

#### Windows Configuration

1. Open the config directory:
   ```
   %APPDATA%\Claude\
   ```

2. Edit `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "karta-markets": {
         "command": "python",
         "args": ["C:\\Users\\YOUR_USERNAME\\karta-markets-mcp\\karta_markets_mcp.py"]
       }
     }
   }
   ```

3. If using a virtual environment:
   ```json
   {
     "mcpServers": {
       "karta-markets": {
         "command": "C:\\Users\\YOUR_USERNAME\\karta-markets-mcp\\venv\\Scripts\\python.exe",
         "args": ["C:\\Users\\YOUR_USERNAME\\karta-markets-mcp\\karta_markets_mcp.py"]
       }
     }
   }
   ```

#### Linux Configuration

1. Edit the config file:
   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```

2. Add the configuration:
   ```json
   {
     "mcpServers": {
       "karta-markets": {
         "command": "python3",
         "args": ["/home/YOUR_USERNAME/karta-markets-mcp/karta_markets_mcp.py"]
       }
     }
   }
   ```

### Restart Claude Desktop

After editing the configuration:
1. Completely quit Claude Desktop (not just close the window)
2. Restart Claude Desktop
3. The Karta Markets tools should now be available

### Verifying Integration

Once configured, you can test by asking Claude:
```
Search for Solana meme coins with the Karta Markets tool
```

If successful, Claude will use the MCP server to search for coins.

## API Configuration

### Connecting to Karta Markets API

To connect to the actual Karta Markets API (when available):

1. **Update the base URL**:
   ```python
   KARTA_API_BASE_URL = "https://api.karta.markets"  # Replace with actual URL
   ```

2. **Add authentication** (if required):
   ```python
   # Add after imports
   KARTA_API_KEY = "your_api_key_here"
   
   # Update the make_api_request function
   async def make_api_request(
       endpoint: str,
       params: Optional[Dict[str, Any]] = None,
       method: str = "GET"
   ) -> Dict[str, Any]:
       url = f"{KARTA_API_BASE_URL}{endpoint}"
       
       headers = {
           "Authorization": f"Bearer {KARTA_API_KEY}",  # Add auth header
           "Content-Type": "application/json"
       }
       
       async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
           try:
               response = await client.request(
                   method=method,
                   url=url,
                   params=params,
                   headers=headers  # Include headers
               )
               response.raise_for_status()
               return response.json()
           except httpx.HTTPStatusError as e:
               return _handle_api_error(e)
   ```

3. **Replace mock data** with actual API calls:
   ```python
   # Before (mock):
   coins = generate_mock_coins_list(params.limit)
   
   # After (actual API):
   response = await make_api_request("/v1/coins/search", api_params)
   coins = response.get('data', [])
   ```

### Environment Variables (Recommended)

For security, use environment variables for sensitive data:

1. **Create a `.env` file**:
   ```bash
   KARTA_API_KEY=your_api_key_here
   KARTA_API_BASE_URL=https://api.karta.markets
   ```

2. **Install python-dotenv**:
   ```bash
   pip install python-dotenv
   ```

3. **Load environment variables**:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   
   KARTA_API_KEY = os.getenv("KARTA_API_KEY")
   KARTA_API_BASE_URL = os.getenv("KARTA_API_BASE_URL", "https://api.karta.markets")
   ```

## Advanced Settings

### Customizing Response Formats

You can add custom formatting functions:

```python
def format_coin_summary(coin: Dict[str, Any]) -> str:
    """Custom formatting for quick summaries."""
    return (
        f"{coin['name']} ({coin['symbol']}): "
        f"{format_currency(coin['price'])} | "
        f"MC: {format_currency(coin['market_cap'])} | "
        f"Vol: {format_currency(coin['volume_24h'])}"
    )
```

### Adding New Tools

To add a custom tool:

```python
class CustomToolInput(BaseModel):
    """Input model for custom tool."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    param1: str = Field(..., description="Parameter description")

@mcp.tool(
    name="karta_custom_tool",
    annotations={
        "title": "Custom Tool",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def custom_tool(params: CustomToolInput) -> str:
    """Tool description."""
    # Implementation
    pass
```

### Performance Tuning

Optimize for different use cases:

```python
# For high-frequency requests
DEFAULT_TIMEOUT = 15.0  # Shorter timeout

# For detailed analysis
MAX_RESULTS = 200  # More results per query

# For rapid scanning
DEFAULT_TIMEOUT = 60.0  # Longer timeout for complex queries
```

## Testing

### Manual Testing

Test each tool individually:

```bash
# Start Python interpreter
python

# Import and test
>>> from karta_markets_mcp import search_coins, SearchCoinsInput
>>> import asyncio
>>> 
>>> # Create test input
>>> params = SearchCoinsInput(
...     min_market_cap=100000,
...     max_market_cap=1000000,
...     limit=5
... )
>>> 
>>> # Run tool
>>> result = asyncio.run(search_coins(params))
>>> print(result)
```

### Automated Testing

Create test scripts:

```python
# test_tools.py
import asyncio
from karta_markets_mcp import (
    search_coins,
    get_coin_details,
    SearchCoinsInput,
    GetCoinDetailsInput
)

async def test_search():
    """Test search functionality."""
    params = SearchCoinsInput(
        min_market_cap=100000,
        limit=10
    )
    result = await search_coins(params)
    assert "Search Results" in result or "coins" in result
    print("✓ Search test passed")

async def test_coin_details():
    """Test coin details retrieval."""
    params = GetCoinDetailsInput(coin_id="test_coin")
    result = await get_coin_details(params)
    assert len(result) > 0
    print("✓ Coin details test passed")

async def run_tests():
    """Run all tests."""
    await test_search()
    await test_coin_details()
    print("\nAll tests passed!")

if __name__ == "__main__":
    asyncio.run(run_tests())
```

Run tests:
```bash
python test_tools.py
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "Module not found" Error

**Problem**: Python can't find required packages

**Solution**:
```bash
# Ensure you're in the correct directory
cd ~/karta-markets-mcp

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Claude Desktop Doesn't Recognize Server

**Problem**: MCP server not appearing in Claude Desktop

**Solution**:
1. Check config file syntax (valid JSON)
2. Verify file paths are absolute
3. Ensure Python path is correct
4. Restart Claude Desktop completely
5. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

#### 3. "Permission Denied" Error

**Problem**: Cannot execute Python script

**Solution**:
```bash
# Make script executable (macOS/Linux)
chmod +x karta_markets_mcp.py

# Or run with python explicitly
python karta_markets_mcp.py
```

#### 4. API Connection Issues

**Problem**: Cannot connect to Karta Markets API

**Solution**:
1. Verify API URL is correct
2. Check internet connection
3. Confirm API key is valid (if required)
4. Review firewall settings
5. Check for rate limiting

#### 5. Timeout Errors

**Problem**: Requests timing out

**Solution**:
```python
# Increase timeout in configuration
DEFAULT_TIMEOUT = 60.0  # Increase from 30.0
```

### Debug Mode

Enable detailed logging:

```python
import logging

# Add at the top of karta_markets_mcp.py
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add logging to functions
async def search_coins(params: SearchCoinsInput) -> str:
    logger.debug(f"Search called with params: {params}")
    # ... rest of function
```

### Getting Additional Help

If issues persist:

1. **Check Logs**: Review MCP server output and Claude Desktop logs
2. **Verify Configuration**: Double-check all configuration files
3. **Test Components**: Test each component (Python, dependencies, API) separately
4. **Community Support**: Reach out to the MCP community or Karta Markets support

## Security Considerations

### Best Practices

1. **Never commit API keys**: Use environment variables or `.env` files
2. **Add to .gitignore**:
   ```
   .env
   *.pyc
   __pycache__/
   venv/
   ```
3. **Use HTTPS**: Ensure all API calls use secure connections
4. **Validate inputs**: Pydantic models automatically validate all inputs
5. **Rate limiting**: Implement rate limiting for production use

### Secure API Key Storage

```python
# Good: Environment variable
KARTA_API_KEY = os.getenv("KARTA_API_KEY")

# Bad: Hardcoded in source
KARTA_API_KEY = "sk_live_123456789"  # Never do this!
```

## Next Steps

After successful configuration:

1. **Explore Tools**: Try each tool with different parameters
2. **Create Workflows**: Combine tools for complex analysis
3. **Customize**: Modify formatting or add custom tools
4. **Integrate**: Connect with other MCP servers for comprehensive workflows
5. **Monitor**: Track performance and optimize as needed

---

For additional support or feature requests, please visit the project repository or contact Karta Markets support.
