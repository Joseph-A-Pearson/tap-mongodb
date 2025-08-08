"""Tests standard tap features using the built-in SDK tests library."""
import os

from singer_sdk.testing import get_standard_tap_tests

from tap_mongodb.tap import TapMongoDB, should_exclude_collection

BASE_CONFIG = {
    "mongo": {"host": "mongodb://frank:1234@github.com/test?retryWrites=true&w=majority"},
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    os.environ["TAP_MONGO_TEST_NO_DB"] = "1"
    tests = get_standard_tap_tests(TapMongoDB, config=BASE_CONFIG)
    for test in tests:
        test()


def test_should_exclude_collection():
    """Test the should_exclude_collection function."""
    # Test exact matches
    assert should_exclude_collection("user_hourly_activity", ["user_hourly_activity"]) is True
    assert should_exclude_collection("other_collection", ["user_hourly_activity"]) is False
    
    # Test wildcard patterns
    assert should_exclude_collection("user_hourly_activity_2024", ["user_hourly_activity*"]) is True
    assert should_exclude_collection("user_hourly_activity_jan", ["user_hourly_activity*"]) is True
    assert should_exclude_collection("user_daily_activity", ["user_hourly_activity*"]) is False
    
    # Test multiple patterns
    patterns = ["user_hourly_activity*", "temp_*", "backup_*"]
    assert should_exclude_collection("user_hourly_activity_2024", patterns) is True
    assert should_exclude_collection("temp_collection", patterns) is True
    assert should_exclude_collection("backup_data", patterns) is True
    assert should_exclude_collection("normal_collection", patterns) is False
    
    # Test empty patterns
    assert should_exclude_collection("any_collection", []) is False
