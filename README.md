# 🚀 VivaTech Startup Analyzer

A high-performance AI-powered tool for analyzing and scoring VivaTech startups based on innovation criteria. Features parallel web scraping, intelligent caching, and optional Claude AI integration for semantic analysis.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Performance](https://img.shields.io/badge/Performance-25x%20faster-brightgreen.svg)](#performance)

## ✨ Features

### 🎯 **Core Functionality**
- **Startup Analysis**: Evaluates startups on 4 innovation criteria (0-25 points each)
- **AI-Powered Scoring**: Optional Claude AI integration for semantic analysis
- **Intelligent Tagging**: Automatic classification with industry tags
- **Interactive Dashboard**: Beautiful HTML dashboard with charts and visualizations

### ⚡ **High Performance**
- **Parallel Processing**: Up to 35 concurrent web scraping requests
- **Smart Caching**: Intelligent disk cache to avoid re-scraping
- **25x Speed Improvement**: Complete analysis in 15-30 minutes vs 4+ hours
- **Async Architecture**: Built with modern async/await patterns

### 🔧 **Technical Features**
- **Robust Error Handling**: Graceful fallbacks and retry mechanisms
- **Multiple Output Formats**: JSON data export + HTML dashboard
- **Progress Tracking**: Real-time progress indicators
- **Flexible Configuration**: Customizable concurrency and analysis limits

## 📊 Innovation Scoring Criteria

The analyzer evaluates startups on four key innovation areas:

| Criterion | Description | Score Range |
|-----------|-------------|-------------|
| **📄 Document Digitization** | OCR, scanning, document capture, digital archiving | 0-25 points |
| **⚡ Data Extraction & Analytics** | Data mining, AI processing, intelligence extraction | 0-25 points |
| **🔒 Certification & Trust** | Blockchain, security, authentication, compliance | 0-25 points |
| **🔗 Information Sharing** | Dashboards, APIs, portals, collaboration tools | 0-25 points |

**Total Score**: 0-100 points

## 🏷️ Industry Tags

Startups are automatically classified with relevant tags:

- 🔲 **Edge Computing**: Distributed computing, IoT, real-time processing
- 🌱 **RSE (ESG)**: Sustainability, environment, social responsibility
- ⚠️ **Risk Management**: Cybersecurity, fraud detection, compliance
- 🚀 **Game Changer**: Disruptive technologies, AI, quantum computing
- 🔮 **Prospective**: Future vision, emerging technologies

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Internet connection for web scraping
- VivaTech CSV data file

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vivatech-analyzer.git
   cd vivatech-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Place your data file**
   ```bash
   # Put your VivaTech.csv file in the project directory
   cp /path/to/your/VivaTech.csv .
   ```

### Basic Usage

**Option 1: Automated Script (Recommended)**
```bash
python run_analysis.py
```
Follow the interactive prompts to configure your analysis.

**Option 2: Direct Python Script**
```bash
python vivatech_analyzer.py
```

### Analysis Options

| Mode | Startups | Duration | Use Case |
|------|----------|----------|----------|
| 🏃 **Quick Test** | 50 | ~30 seconds | Testing and demonstrations |
| 📊 **Extended Analysis** | 200 | ~2 minutes | Quality analysis |
| 🚀 **Complete Analysis** | All (~2244) | ~15-30 minutes | Full production run |
| 🎛️ **Custom** | Configurable | Variable | Specific needs |

## 🤖 Claude AI Integration (Optional)

For enhanced semantic analysis, you can integrate with Claude AI:

### Benefits
- **Higher Accuracy**: Semantic understanding vs keyword matching
- **Contextual Analysis**: Better comprehension of startup descriptions
- **Intelligent Tagging**: More accurate industry classification

### Setup
1. Get your Claude API key from [Anthropic](https://console.anthropic.com/)
2. During analysis, enter your API key when prompted
3. The system will automatically save it for future use

### Comparison

| Feature | Without Claude AI | With Claude AI |
|---------|------------------|----------------|
| **Analysis Method** | Keyword matching | Semantic analysis |
| **Accuracy** | Good | Excellent |
| **Speed** | Fast | Fast |
| **Cost** | Free | Anthropic API costs |

## 📈 Performance Benchmarks

### Speed Improvements (V2 vs V1)
- **25x faster** overall processing
- **35x concurrent** web requests
- **Intelligent caching** eliminates redundant work
- **Async architecture** for maximum efficiency

### Example Performance
```
🔥 Performance Results:
   📊 2244 startups analyzed in 28.3 minutes
   ⚡ Scraping: 15.2 minutes (25x improvement)
   🧠 AI Analysis: 13.1 minutes
   💾 Cache hit rate: 23%
   📈 Success rate: 97.8%
```

## 📁 Output Files

After analysis, you'll get:

### 📊 **JSON Data Export**
```
vivatech_analysis_v2_YYYYMMDD_HHMMSS.json
```
Complete structured data including:
- Startup details and scores
- Performance metrics
- Cache statistics
- Tag distribution

### 🌐 **Interactive Dashboard**
```
dashboard_vivatech.html
```
Beautiful HTML dashboard featuring:
- Top 20 startups visualization
- Interactive charts and graphs
- Performance statistics
- Detailed startup listings

## 🛠️ Configuration

### Environment Variables
```bash
# Optional: Set default Claude API key
export CLAUDE_API_KEY="your-api-key-here"
```

### Configuration File
Create `.claude_config.json` for persistent API key storage:
```json
{
  "api_key": "your-claude-api-key"
}
```

### Custom Analysis
```python
from vivatech_analyzer import VivaTechAnalyzerV2

# Initialize with custom settings
analyzer = VivaTechAnalyzerV2(
    csv_file_path='your_data.csv',
    claude_api_key='optional-api-key'
)

# Run custom analysis
await analyzer.analyze_startups_async(
    limit=100,           # Number of startups
    max_concurrent=20    # Parallel requests
)
```

## 📋 CSV Data Format

Your VivaTech CSV should include these columns:

| Column | Description | Required |
|--------|-------------|----------|
| `HOST COMPANY NAME` | Startup/company name | ✅ Yes |
| `WEBSITE` | Company website URL | ✅ Yes |
| `DESCRIPTION` | Company description | ✅ Yes |
| `HALL` | VivaTech hall location | ❌ No |
| `DAYS OF PRESENCE` | Event attendance days | ❌ No |
| `BUSINESS-SECTOR` | Industry sector | ❌ No |
| `COUNTRY` | Company country | ❌ No |

## 🔧 Troubleshooting

### Common Issues

**❌ "No module named 'xxx'"**
```bash
pip install -r requirements.txt
```

**❌ "VivaTech.csv not found"**
- Ensure the CSV file is in the project directory
- Check file name spelling and case sensitivity

**❌ "SSL Certificate errors"**
```bash
pip install --upgrade certifi
```

**❌ "Claude API errors"**
- Verify your API key is correct
- Check your Anthropic account credits
- The system will fallback to keyword analysis

### Performance Tuning

**For slower connections:**
```python
# Reduce concurrency
max_concurrent=10
```

**For faster processing:**
```python
# Increase concurrency (if your system can handle it)
max_concurrent=50
```

**Memory usage:**
```python
# For large datasets, process in smaller batches
limit=500  # Process 500 startups at a time
```

## 🏗️ Architecture

### Core Components

```
vivatech_analyzer.py          # Main analyzer class
├── VivaTechAnalyzerV2       # Primary analysis engine
├── AsyncWebScraper          # High-performance web scraping
├── CacheManager            # Intelligent caching system
└── ClaudeAnalyzer          # AI semantic analysis

run_analysis.py              # User-friendly automation script
generate_dashboard_from_json.py  # Dashboard generator utility
```

### Data Flow
```
CSV Data → Web Scraping → Content Analysis → AI Scoring → Results Export
    ↓           ↓              ↓             ↓            ↓
Input Validation → Cache Check → Semantic Analysis → Tag Assignment → Dashboard Generation
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/yourusername/vivatech-analyzer.git
cd vivatech-analyzer
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black vivatech_analyzer.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **VivaTech** for providing the startup ecosystem data
- **Anthropic** for Claude AI capabilities
- **Open Source Community** for the amazing Python libraries

## 📞 Support

- 📧 **Email**: support@yourproject.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/vivatech-analyzer/issues)
- 📖 **Documentation**: [Full Documentation](https://docs.yourproject.com)

---

**Made with ❤️ for the VivaTech innovation ecosystem**

*Analyze smarter, not harder! 🚀*