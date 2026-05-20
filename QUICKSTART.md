# Quick Start Guide - Karta Markets MCP Server

Get up and running with the Karta Markets MCP server in 5 minutes!

## 🚀 Quick Setup

### 1. Install Python (if needed)

```bash
python --version  # Should be 3.10 or higher
```

### 2. Download Files

Create a folder and download these files:
- `karta_markets_mcp.py`
- `requirements.txt`

### 3. Install Dependencies

```bash
cd /path/to/karta-markets-mcp
pip install -r requirements.txt
```

### 4. Test It Works

```bash
python karta_markets_mcp.py --help
```

You should see help information about the server.

### 5. Configure Claude Desktop

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this:
```json
{
  "mcpServers": {
    "karta-markets": {
      "command": "python",
      "args": ["/FULL/PATH/TO/karta_markets_mcp.py"]
    }
  }
}
```

Replace `/FULL/PATH/TO/` with the actual path!

### 6. Restart Claude Desktop

Completely quit and restart Claude Desktop.

## ✅ Test It's Working

Ask Claude:
```
Search for Solana meme coins using Karta Markets
```

If you see results, congratulations! 🎉

## 📖 Quick Examples

### Find coins in a specific market cap range:
```
Find meme coins with market cap between $100K and $1M
```

### Search for high-volume coins:
```
Show me Solana meme coins with at least $50K in 24h volume
```

### Get trending coins:
```
What are the top 10 trending Solana meme coins right now?
```

### Look up a specific coin:
```
Get details for coin with address: [contract-address]
```

### View price history:
```
Show me the 7-day price history for BONK
```

## 🔧 Troubleshooting

**Server not showing in Claude?**
- Check that the path in the config file is absolute (not relative)
- Make sure you completely quit and restarted Claude Desktop
- Verify the JSON syntax is correct (use a JSON validator)

**Python errors?**
- Make sure you're using Python 3.10 or higher
- Try running in a virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

**Need more help?**
See the full README.md or CONFIGURATION_GUIDE.md

## 🎯 Next Steps

Once it's working:
1. Explore different search parameters
2. Try combining multiple filters
3. Experiment with JSON format for programmatic use
4. Check out the full documentation for advanced features

---

**That's it!** You're ready to track Solana meme coins with AI assistance.
