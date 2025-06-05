# 📖 Usage Guide

This guide provides practical examples and detailed usage instructions for the VivaTech Startup Analyzer.

## 🚀 Quick Start Examples

### Example 1: Basic Analysis (Recommended for First Use)

```bash
# 1. Place your VivaTech.csv file in the project directory
cp /path/to/your/VivaTech.csv .

# 2. Run the automated analysis
python run_analysis.py

# 3. Follow the prompts:
#    - Configure Claude API (optional but recommended)
#    - Choose analysis mode (start with "Quick Test")
#    - Wait for completion and view results
```

### Example 2: Custom Analysis

```python
import asyncio
from vivatech_analyzer import VivaTechAnalyzerV2

async def analyze_custom():
    # Initialize analyzer
    analyzer = VivaTechAnalyzerV2(
        csv_file_path='VivaTech.csv',
        claude_api_key='your-api-key-here'  # Optional
    )
    
    # Load data
    if not analyzer.load_data():
        print("Failed to load data")
        return
    
    # Run custom analysis
    await analyzer.analyze_startups_async(
        limit=100,           # Analyze 100 startups
        max_concurrent=20    # 20 parallel requests
    )
    
    # Show results
    analyzer.print_top_recommendations(15)
    
    # Export results
    json_file = analyzer.export_results_v2()
    html_file = analyzer.generate_dashboard_v2()
    
    print(f"Results saved to: {json_file} and {html_file}")

# Run the analysis
asyncio.run(analyze_custom())
```

### Example 3: Generate Dashboard from Existing Data

```bash
# If you already have analysis results, generate a new dashboard
python generate_dashboard_from_json.py
```

## 🎯 Use Cases

### Use Case 1: VivaTech Event Planning

**Scenario**: You're attending VivaTech and want to identify the most relevant startups to visit.

**Solution**:
```bash
# Run quick analysis for event planning
python run_analysis.py
# Choose option 2: Extended Analysis (200 startups, ~2 minutes)
```

**Output**: 
- Interactive dashboard with top 20 startups
- Hall and presence day information
- Contact details for scheduling meetings

### Use Case 2: Investment Scouting

**Scenario**: You're an investor looking for innovative startups in specific domains.

**Solution**:
```python
# Focus on specific innovation criteria
from vivatech_analyzer import VivaTechAnalyzerV2

async def investment_analysis():
    analyzer = VivaTechAnalyzerV2('VivaTech.csv', claude_api_key='your-key')
    await analyzer.analyze_startups_async(limit=500, max_concurrent=30)
    
    # Filter by high scores and specific tags
    top_startups = sorted(analyzer.scored_startups, 
                         key=lambda x: x['total_score'], reverse=True)
    
    # Focus on Game Changers with high scores
    game_changers = [s for s in top_startups 
                    if 'Game Changer' in s['claude_analysis'].get('tags', [])
                    and s['total_score'] > 60]
    
    print(f"Found {len(game_changers)} high-potential Game Changer startups")
    for startup in game_changers[:10]:
        print(f"- {startup['name']}: {startup['total_score']:.1f} points")

asyncio.run(investment_analysis())
```

### Use Case 3: Technology Trend Analysis

**Scenario**: You want to understand innovation trends in the VivaTech ecosystem.

**Solution**:
```bash
# Run complete analysis for comprehensive insights
python run_analysis.py
# Choose option 3: Complete Analysis (all startups)
```

**Analysis Steps**:
1. Review tag distribution in the dashboard
2. Examine JSON export for detailed trend data
3. Identify emerging technology patterns
4. Compare scores across different sectors

## 🔧 Advanced Configuration

### Custom Scoring Weights

Modify the scoring algorithm by editing `vivatech_analyzer.py`:

```python
# In the ClaudeAnalyzer._fallback_analysis method
keywords_mapping = {
    "numerisation": ["ocr", "document", "scan", "your_custom_keywords"],
    "extraction": ["data mining", "analytics", "your_domain_specific_terms"],
    "certification": ["blockchain", "security", "compliance", "your_trust_keywords"],
    "mise_disposition": ["dashboard", "api", "portal", "your_sharing_terms"]
}

# Adjust scoring multiplier (current: score * 2.5, max 25)
scores[criterion] = min(score * 3.0, 25)  # Increase sensitivity
```

### Performance Optimization

**For slower networks:**
```python
# Reduce concurrency and increase timeout
async with AsyncWebScraper(max_concurrent=10, timeout=20) as scraper:
    results = await scraper.scrape_websites_batch(urls)
```

**For powerful servers:**
```python
# Increase concurrency for faster processing
await analyzer.analyze_startups_async(limit=None, max_concurrent=50)
```

**For memory-constrained environments:**
```python
# Process in smaller batches
for i in range(0, total_startups, 200):
    batch = df.iloc[i:i+200]
    await analyzer.analyze_startups_async(limit=200)
    # Save intermediate results
```

## 📊 Understanding Results

### Score Interpretation

| Score Range | Interpretation | Action |
|-------------|---------------|--------|
| 80-100 | Highly relevant | Priority meetings |
| 60-79 | Very relevant | Strong candidates |
| 40-59 | Moderately relevant | Worth exploring |
| 20-39 | Somewhat relevant | Secondary priority |
| 0-19 | Low relevance | Optional consideration |

### Tag Meanings

- **🔲 Edge Computing**: Real-time processing, IoT, distributed systems
- **🌱 RSE (ESG)**: Environmental, social, governance focus
- **⚠️ Risk Management**: Security, compliance, fraud prevention
- **🚀 Game Changer**: Disruptive innovation, breakthrough technology
- **🔮 Prospective**: Future-focused, emerging technologies

### Dashboard Features

1. **Top 20 Visualization**: Horizontal bar chart with scores
2. **Tag Distribution**: Pie chart showing technology trends
3. **Performance Stats**: Cache hits, success rates, AI usage
4. **Detailed Listings**: Complete startup information with links

## 🛠️ Troubleshooting Common Issues

### Issue 1: Low Success Rate

**Symptoms**: Many failed scrapes, low success rate
**Solutions**:
```python
# Increase timeout and reduce concurrency
AsyncWebScraper(max_concurrent=5, timeout=30)

# Check network connectivity
ping google.com

# Verify CSV URL format
# Ensure URLs start with http:// or https://
```

### Issue 2: Claude API Errors

**Symptoms**: "Claude API errors" in logs
**Solutions**:
```bash
# Verify API key
echo $CLAUDE_API_KEY

# Check account credits at https://console.anthropic.com/
# The system automatically falls back to keyword analysis
```

### Issue 3: Memory Issues

**Symptoms**: Out of memory errors, slow performance
**Solutions**:
```python
# Process smaller batches
analyzer.analyze_startups_async(limit=100)

# Clear cache periodically
rm -rf ./cache/

# Monitor memory usage
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")
```

## 📈 Performance Benchmarks

### Typical Performance (MacBook Pro M1)

| Dataset Size | Time (No Cache) | Time (With Cache) | Success Rate |
|-------------|----------------|-------------------|--------------|
| 50 startups | 45 seconds | 20 seconds | 95%+ |
| 200 startups | 3 minutes | 1.5 minutes | 94%+ |
| 1000 startups | 15 minutes | 8 minutes | 93%+ |
| 2244 startups | 28 minutes | 18 minutes | 92%+ |

### Optimization Tips

1. **Use caching**: Significant speedup on repeated runs
2. **Optimal concurrency**: 20-35 for most networks
3. **Claude API**: Improves accuracy, minimal speed impact
4. **SSD storage**: Faster cache operations
5. **Stable network**: Reduces retry overhead

## 🎯 Best Practices

### For Event Preparation
1. Run analysis 1-2 days before VivaTech
2. Use Extended Analysis (200 startups) for good coverage
3. Export dashboard for offline viewing
4. Create meeting schedules based on hall/day information

### For Investment Analysis
1. Use Complete Analysis for comprehensive coverage
2. Enable Claude AI for better accuracy
3. Focus on startups with scores >60
4. Cross-reference with sector-specific criteria

### For Research & Trends
1. Run periodic analyses to track evolution
2. Compare tag distributions over time
3. Monitor emerging technology patterns
4. Export JSON for further data analysis

## 💡 Tips & Tricks

### Keyboard Shortcuts
- `Ctrl+C`: Stop analysis gracefully
- `Enter`: Use default options in prompts

### Command Line Automation
```bash
# Unattended analysis with defaults
echo -e "n\n1\nn" | python run_analysis.py

# Quick dashboard regeneration
python generate_dashboard_from_json.py
```

### Data Export Integration
```python
# Export to different formats
import json
import pandas as pd

# Load results
with open('vivatech_analysis_v2_*.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame for analysis
df = pd.DataFrame(data['top_startups'])

# Export to Excel
df.to_excel('vivatech_results.xlsx', index=False)

# Export filtered results
high_scores = df[df['total_score'] > 60]
high_scores.to_csv('high_potential_startups.csv', index=False)
```

---

**Need more help?** Check the main [README.md](README.md) or open an issue on GitHub!