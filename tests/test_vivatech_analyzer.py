import pytest
import time
from datetime import datetime, timedelta

# Assuming vivatech_analyzer.py is in the parent directory or PYTHONPATH is set up
# For this subtask, we'll assume it can be imported directly.
# In a real scenario, project structure (e.g., src/ layout) or pytest path manipulation might be needed.
from vivatech_analyzer import CacheManager, ClaudeAnalyzer # Adjusted import

# --- Tests for CacheManager ---

@pytest.fixture
def cache_manager(tmp_path):
    # Use a temporary directory for the cache during tests
    return CacheManager(cache_dir=str(tmp_path / "test_cache"), cache_duration_days=1)

def test_cache_key_generation(cache_manager):
    url1 = "http://example.com"
    url2 = "http://example.com"
    url3 = "http://different-example.com"
    assert cache_manager.get_cache_key(url1) == cache_manager.get_cache_key(url2)
    assert cache_manager.get_cache_key(url1) != cache_manager.get_cache_key(url3)
    assert isinstance(cache_manager.get_cache_key(url1), str)

def test_cache_set_and_get(cache_manager):
    url = "http://test.com/page"
    content = {"title": "Test Page", "content": "Some data"}

    # Test caching content
    cache_manager.cache_content(url, content)

    # Test retrieving cached content
    cached_item = cache_manager.get_cached_content(url)
    assert cached_item is not None
    assert cached_item["title"] == "Test Page"
    assert cached_item["content"] == "Some data"

def test_cache_get_non_existent(cache_manager):
    url = "http://nonexistent.com"
    assert cache_manager.get_cached_content(url) is None

def test_cache_expiry(cache_manager):
    url = "http://expired.com"
    content = {"data": "to_expire"}

    cache_manager.cache_content(url, content)

    # Manually manipulate the cache entry's timestamp to simulate expiry
    # This is a way to test expiry logic without waiting.
    # Note: This depends on the internal structure of how diskcache stores metadata.
    # A more robust way might involve mocking `datetime.now()` if CacheManager allowed it.

    cache_key = cache_manager.get_cache_key(url)
    cached_entry = cache_manager.cache.get(cache_key) # read_stats=False for some versions
    if cached_entry and 'timestamp' in cached_entry:
        two_days_ago = (datetime.now() - timedelta(days=2)).isoformat()
        cached_entry['timestamp'] = two_days_ago
        cache_manager.cache.set(cache_key, cached_entry) # Overwrite with modified timestamp

    assert cache_manager.get_cached_content(url) is None, "Cache should have expired"

def test_cache_content_remains_if_not_expired(cache_manager):
    url = "http://not-expired.com"
    content = {"data": "fresh_data"}
    cache_manager.cache_content(url, content)

    # To ensure it's not immediately expiring, we can try to get it
    # This doesn't directly test the non-expiry over time, but that it works within duration
    assert cache_manager.get_cached_content(url) is not None


# --- Tests for ClaudeAnalyzer._fallback_analysis ---

@pytest.fixture
def claude_analyzer_no_key():
    # Initialize ClaudeAnalyzer without an API key to force fallback
    return ClaudeAnalyzer(api_key=None)

def test_fallback_analysis_scoring_and_tags(claude_analyzer_no_key):
    content = "This startup focuses on document digitization using OCR and advanced data mining for analytics."
    description = "We offer solutions for paper archival and information extraction."

    analysis = claude_analyzer_no_key._fallback_analysis(content, description)

    assert "scores" in analysis
    assert "total_score" in analysis
    assert "tags" in analysis
    assert "justification" in analysis
    assert analysis["justification"] == "Analyse par mots-clés (Claude indisponible)"

    # Check specific criteria scores (exact scores depend on keyword counts and multipliers)
    # These assertions are examples; actual values would need to be calculated based on the keyword list
    assert analysis["scores"]["numerisation"] > 0
    assert analysis["scores"]["extraction"] > 0
    assert analysis["scores"]["certification"] == 0 # No keywords for this
    assert analysis["scores"]["mise_disposition"] == 0 # No keywords for this

    total_score_calculated = sum(analysis["scores"].values())
    assert analysis["total_score"] == total_score_calculated

    # Check for expected tags based on keywords in content/description
    # This depends on the _assign_fallback_tags logic and keywords
    # Example: if "analytics" or "data mining" maps to "Game Changer" or similar
    # For this example, let's assume no specific tags are hit by the limited keywords above
    # A more thorough test would use text designed to hit specific tags.

    # Example: if "ocr" or "analytics" triggered a tag
    # Based on current _assign_fallback_tags, "analytics" isn't a direct trigger.
    # "data mining" could be part of "Game Changer" if "innovation" keywords were present.
    # Let's test a specific tag:
    content_for_tags = "Our innovative AI solution is a game changer for cybersecurity and risk management."
    description_for_tags = "We use edge computing for sustainability."

    analysis_tags = claude_analyzer_no_key._fallback_analysis(content_for_tags, description_for_tags)
    assert "Game Changer" in analysis_tags["tags"]
    assert "Risque augmenté" in analysis_tags["tags"]
    assert "Edge computing" in analysis_tags["tags"]
    assert "RSE" in analysis_tags["tags"]


def test_fallback_analysis_no_matching_keywords(claude_analyzer_no_key):
    content = "This is a generic website about unrelated topics."
    description = "We sell flowers."

    analysis = claude_analyzer_no_key._fallback_analysis(content, description)

    assert analysis["scores"]["numerisation"] == 0
    assert analysis["scores"]["extraction"] == 0
    assert analysis["scores"]["certification"] == 0
    assert analysis["scores"]["mise_disposition"] == 0
    assert analysis["total_score"] == 0
    assert len(analysis["tags"]) == 0 # Expect no tags if no relevant keywords

def test_fallback_analysis_score_normalization(claude_analyzer_no_key):
    # Create content with many repeated keywords for a single criterion
    keyword = "ocr " # From "numerisation"
    content = keyword * 50 # Should give a high raw score
    description = "More ocr."

    analysis = claude_analyzer_no_key._fallback_analysis(content, description)

    # Max score for any criterion is 25
    assert analysis["scores"]["numerisation"] <= 25.0
    assert analysis["scores"]["numerisation"] > 0

    # Check that total score reflects this
    assert analysis["total_score"] == analysis["scores"]["numerisation"] # Since other scores should be 0
