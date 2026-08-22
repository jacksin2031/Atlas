import pathlib

# Fix integration __init__.py to import from bridges module directly
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\integration\__init__.py")
p.write_text("from atlas_ai.integration.bridges import IPCAIBridge, WorkflowAIBridge, VisionAIBridge\n__all__ = [\"IPCAIBridge\", \"WorkflowAIBridge\", \"VisionAIBridge\"]\n", encoding="utf-8")

# Fix resources __init__.py
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\resources\__init__.py")
p.write_text("from atlas_ai.resources.manager import AIResourceManager, LRUCache, TempBuffer\n__all__ = [\"AIResourceManager\", \"LRUCache\", \"TempBuffer\"]\n", encoding="utf-8")

# Fix metrics __init__.py
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\metrics\__init__.py")
p.write_text("from atlas_ai.metrics.collector import AIMetricsCollector, Counter, Gauge, Histogram\n__all__ = [\"AIMetricsCollector\", \"Counter\", \"Gauge\", \"Histogram\"]\n", encoding="utf-8")

# Fix health __init__.py
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\health\__init__.py")
p.write_text("from atlas_ai.health.service import AIHealthService, HealthStatus\n__all__ = [\"AIHealthService\", \"HealthStatus\"]\n", encoding="utf-8")

# Fix security __init__.py
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\security\__init__.py")
p.write_text("from atlas_ai.security.permissions import SecurityValidator, SecurityPolicy, Permission\n__all__ = [\"SecurityValidator\", \"SecurityPolicy\", \"Permission\"]\n", encoding="utf-8")

# Fix storage __init__.py
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\storage\__init__.py")
p.write_text("from atlas_ai.storage.abstraction import AIStorageAdapter, StorageDomain, StorageBackend\n__all__ = [\"AIStorageAdapter\", \"StorageDomain\", \"StorageBackend\"]\n", encoding="utf-8")

# Fix registry __init__.py
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\src\atlas_ai\registry\__init__.py")
p.write_text("from atlas_ai.registry.ai_registry import AIRegistry\n__all__ = [\"AIRegistry\"]\n", encoding="utf-8")

print("Fixed all sub-package __init__.py files")
