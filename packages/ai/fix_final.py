import pathlib
import re

# Fix services.py - add HealthStatus import
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\services.py")
content = p.read_text(encoding="utf-8")
# Add HealthStatus to imports
content = content.replace(
    "from atlas_ai.health.service import HealthService, HealthStatus",
    "from atlas_ai.health.service import HealthService, HealthStatus"
)
# Check if it's already there
if "from atlas_ai.health.service import HealthStatus" not in content:
    # Add the import near the top
    content = content.replace(
        "from atlas_ai.errors import",
        "from atlas_ai.errors import\nfrom atlas_ai.health.service import HealthStatus"
    )
p.write_text(content, encoding="utf-8")
print("Fixed services.py HealthStatus import")

# Fix LRUCache - the issue is that accessing 'a' moves it to the end, so when 'c' is added, 'b' (not 'a') gets evicted
# The test expects 'a' to be evicted but LRU puts accessed items at the end
# Let's check the actual behavior
print("LRUCache test expects 'a' to be evicted after putting 'c', but 'a' was accessed so it moves to end")
print("Need to fix the test, not the cache")
