# Karta Markets MCP Server - Usage Examples

This document provides practical examples of using the Karta Markets MCP server for various cryptocurrency tracking and analysis scenarios.

## Table of Contents

1. [Basic Searches](#basic-searches)
2. [Advanced Filtering](#advanced-filtering)
3. [Market Analysis](#market-analysis)
4. [Trading Strategies](#trading-strategies)
5. [Portfolio Management](#portfolio-management)
6. [Research & Discovery](#research--discovery)

---

## Basic Searches

### Example 1: Simple Search
**Goal**: Find any Solana meme coins

**Prompt**:
```
Search for Solana meme coins
```

**What happens**: Returns top 20 coins sorted by market cap

---

### Example 2: Search by Name
**Goal**: Find coins with "dog" in the name

**Prompt**:
```
Search for meme coins with "dog" in the name
```

**Parameters used**:
- `query: "dog"`
- Default limit (20 coins)

---

### Example 3: Get Coin Details
**Goal**: Deep dive into a specific coin

**Prompt**:
```
Get detailed information for coin: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

**Returns**: Complete coin data including:
- Current price
- Market cap
- Volume statistics
- Holder count
- Contract information
- Historical metrics

---

## Advanced Filtering

### Example 4: Market Cap Range Filter
**Goal**: Find mid-cap meme coins

**Prompt**:
```
Find Solana meme coins with market cap between $500,000 and $5,000,000
```

**Parameters used**:
- `min_market_cap: 500000`
- `max_market_cap: 5000000`
- `sort_by: "market_cap"`
- `sort_order: "desc"`

---

### Example 5: Volume-Based Search
**Goal**: Identify actively traded coins

**Prompt**:
```
Show me meme coins with at least $100,000 in 24-hour trading volume
```

**Parameters used**:
- `min_volume_24h: 100000`
- `sort_by: "volume"`
- `sort_order: "desc"`

---

### Example 6: Multi-Criteria Filter
**Goal**: Find coins meeting multiple requirements

**Prompt**:
```
Find Solana meme coins that have:
- Market cap between $100K and $1M
- At least $50K in 24h volume
- More than 1000 holders
- Sort by price change (biggest gainers first)
```

**Parameters used**:
- `min_market_cap: 100000`
- `max_market_cap: 1000000`
- `min_volume_24h: 50000`
- `min_holders: 1000`
- `sort_by: "price_change"`
- `sort_order: "desc"`

---

### Example 7: Micro-Cap Gems
**Goal**: Find very small cap coins with potential

**Prompt**:
```
Search for meme coins with market cap under $100K but with decent volume (>$10K)
```

**Parameters used**:
- `max_market_cap: 100000`
- `min_volume_24h: 10000`
- `sort_by: "price_change"`
- `limit: 50`

---

## Market Analysis

### Example 8: Trending Analysis
**Goal**: Identify what's hot right now

**Prompt**:
```
What are the top 20 trending Solana meme coins in the last 24 hours?
```

**Parameters used**:
- `limit: 20`
- `time_frame: "24h"`

**Use case**: Quick market pulse check

---

### Example 9: Price History Analysis
**Goal**: Study price movements over time

**Prompt**:
```
Show me the 7-day price history for BONK with detailed data points
```

**Parameters used**:
- `coin_id: "BONK"`
- `time_frame: "7d"`
- `response_format: "json"` (for detailed analysis)

**Returns**: Time-series data with timestamps, prices, and volumes

---

### Example 10: Market Overview
**Goal**: Get the big picture

**Prompt**:
```
Give me an overview of the Solana meme coin market
```

**Returns**:
- Total market capitalization
- 24h trading volume
- Number of tracked coins
- Trending coin count

---

## Trading Strategies

### Example 11: Momentum Trading
**Goal**: Find coins with strong recent gains

**Prompt**:
```
Find meme coins with the highest 24h price increase, minimum $25K volume
```

**Parameters used**:
- `min_volume_24h: 25000`
- `sort_by: "price_change"`
- `sort_order: "desc"`
- `limit: 30`

**Strategy**: Ride momentum on high-volume gainers

---

### Example 12: Value Hunting
**Goal**: Find undervalued coins with growing interest

**Prompt**:
```
Show me coins with:
- Market cap under $500K
- Increasing volume (>$20K in 24h)
- At least 500 holders
- Sort by holder count
```

**Parameters used**:
- `max_market_cap: 500000`
- `min_volume_24h: 20000`
- `min_holders: 500`
- `sort_by: "holders"`
- `sort_order: "desc"`

**Strategy**: Find coins gaining traction before they pump

---

### Example 13: Liquidity Focus
**Goal**: Ensure you can exit positions

**Prompt**:
```
Find meme coins with high volume relative to market cap (min $100K volume, max $2M market cap)
```

**Parameters used**:
- `min_volume_24h: 100000`
- `max_market_cap: 2000000`
- `sort_by: "volume"`

**Strategy**: High volume-to-cap ratio = good liquidity

---

### Example 14: Established Coins
**Goal**: Find more stable, proven meme coins

**Prompt**:
```
Show me meme coins with:
- Market cap over $5M
- High holder count (>10,000)
- Consistent volume
```

**Parameters used**:
- `min_market_cap: 5000000`
- `min_holders: 10000`
- `min_volume_24h: 100000`
- `sort_by: "market_cap"`

**Strategy**: Lower risk, established projects

---

## Portfolio Management

### Example 15: Portfolio Diversity Check
**Goal**: Track holdings across different market cap tiers

**Multi-step process**:

```
Step 1: Get your micro-caps (<$500K)
Search for my holdings with max market cap $500K

Step 2: Get your mid-caps ($500K-$5M)
Search for my holdings with market cap between $500K and $5M

Step 3: Get your large-caps (>$5M)
Search for my holdings with min market cap $5M
```

---

### Example 16: Performance Tracking
**Goal**: Monitor daily changes in holdings

```
Get the 24-hour performance for coins: [list of contract addresses]
```

Repeat for each coin:
```
Get details for coin: [contract-address]
```

Check `price_change_24h` field for each

---

### Example 17: Entry Point Identification
**Goal**: Find good entry points based on recent pullbacks

**Prompt**:
```
Find established meme coins (>$1M market cap) that are down 10-30% in the last 24h with good volume
```

**Parameters used**:
- `min_market_cap: 1000000`
- `min_volume_24h: 50000`
- `sort_by: "price_change"`
- `sort_order: "asc"` (ascending to see biggest declines first)

**Strategy**: Buy the dip on quality projects

---

## Research & Discovery

### Example 18: New Coin Discovery
**Goal**: Find recently launched coins

**Prompt**:
```
Show me the newest meme coins with at least $10K volume (sorted by age)
```

**Parameters used**:
- `min_volume_24h: 10000`
- `sort_by: "age"`
- `sort_order: "asc"`
- `limit: 50`

**Use case**: Early bird catches the worm

---

### Example 19: Comparative Analysis
**Goal**: Compare similar coins

**Multi-step process**:
```
Step 1: Find coins in similar category
Search for meme coins with "cat" in the name

Step 2: Get detailed stats for each
For each result, get full details

Step 3: Compare metrics
- Market cap
- Volume
- Holders
- Price changes
```

---

### Example 20: Risk Assessment
**Goal**: Evaluate coin health before investing

**Checklist using MCP tools**:
```
1. Get coin details: Basic metrics check
   - What's the market cap?
   - How many holders?
   - What's the volume?

2. Check price history (7d): Volatility assessment
   - Is it stable or erratic?
   - Any suspicious pump patterns?

3. Compare to similar coins: Market position
   - Is this coin overvalued vs peers?
   - How does volume compare?

4. Check trending status: Community interest
   - Is it trending?
   - Is momentum building or fading?
```

---

## Advanced Use Cases

### Example 21: Whale Watching (High Holder Count)
**Goal**: Find coins with broad distribution

**Prompt**:
```
Find meme coins with more than 5,000 holders, sorted by holder count
```

**Parameters used**:
- `min_holders: 5000`
- `sort_by: "holders"`
- `sort_order: "desc"`

**Insight**: More holders often means more stable price

---

### Example 22: Volume Spike Detection
**Goal**: Find unusual trading activity

**Prompt**:
```
Show me coins with volume over $200K (to find anomalies)
```

**Parameters used**:
- `min_volume_24h: 200000`
- `sort_by: "volume"`

**Use case**: High volume can signal news or upcoming moves

---

### Example 23: Dead Cat Bounce Detection
**Goal**: Avoid falling knives

**Multi-step**:
```
Step 1: Find coins with major declines
Get coins sorted by price change (ascending)

Step 2: Check volume
Are declining coins also seeing volume spikes?

Step 3: Check history
Look at 7-day chart - is this a bounce or continuous decline?
```

---

### Example 24: Diversification Strategy
**Goal**: Build a balanced meme coin portfolio

**Prompt sequence**:
```
# 30% Large-cap exposure
Find top 5 meme coins by market cap with >$10M market cap

# 40% Mid-cap exposure
Find 8 coins with market cap between $1M-$10M, high volume

# 20% Small-cap growth
Find 5 coins with market cap $100K-$1M, growing holder count

# 10% Micro-cap lottery tickets
Find 2-3 coins under $100K with decent volume
```

---

### Example 25: JSON Export for Analysis
**Goal**: Get raw data for spreadsheet or custom tools

**Prompt**:
```
Search for top 50 meme coins, return in JSON format
```

**Parameters used**:
- `limit: 50`
- `response_format: "json"`

**Result**: Structured data you can:
- Import into Excel/Google Sheets
- Process with Python/JavaScript
- Feed into custom dashboards
- Archive for historical tracking

---

## Tips for Effective Use

### 1. Start Broad, Then Narrow
```
Step 1: "Show me all meme coins"
Step 2: "Now filter for market cap >$500K"
Step 3: "From those, show me ones with >$50K volume"
```

### 2. Use Multiple Metrics
Don't just look at price! Consider:
- Market cap (project size)
- Volume (liquidity)
- Holders (distribution)
- Price change (momentum)

### 3. Regular Monitoring
Set up recurring queries:
- Daily: Check trending coins
- Weekly: Review portfolio performance
- Monthly: Discover new opportunities

### 4. Combine with External Research
Use MCP data as starting point, then:
- Check social media sentiment
- Read project documentation
- Verify contract on blockchain explorers
- Join community channels

### 5. Document Your Process
Keep track of:
- Why you filtered certain ways
- What worked and what didn't
- Coins you're watching
- Entry/exit criteria

---

## Common Workflows

### Quick Scan (5 minutes)
1. Get market overview
2. Check trending coins
3. Review any significant movers

### Deep Dive (30 minutes)
1. Search with specific criteria
2. Get details on top candidates
3. Review price history
4. Compare to similar coins
5. Make decision

### Portfolio Review (15 minutes)
1. Get details for each holding
2. Check 24h performance
3. Review any significant changes
4. Rebalance if needed

---

## Conclusion

These examples demonstrate the flexibility and power of the Karta Markets MCP server. By adjusting parameters and combining different tools, you can create custom workflows that match your specific trading style and research needs.

Remember:
- **Always verify data** - Use multiple sources
- **Do your own research** - MCP tools are helpers, not investment advisors
- **Start small** - Test strategies with small amounts
- **Stay informed** - Markets change quickly

Happy tracking! 🚀
