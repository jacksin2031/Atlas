import pathlib
p = pathlib.Path(r"E:\資料夾\桌面\Atlas\packages\ai\tests\test_unit.py")
content = p.read_text(encoding="utf-8")

# Fix the LRU cache test - accessing 'a' moves it to the end, so 'b' gets evicted
old_test = """    def test_lru_cache(self) -> None:
        cache = LRUCache(max_size=2)
        cache.put('a', 1)
        cache.put('b', 2)
        self.assertEqual(cache.get('a'), 1)
        cache.put('c', 3)
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.size, 2)"""

new_test = """    def test_lru_cache(self) -> None:
        cache = LRUCache(max_size=2)
        cache.put('a', 1)
        cache.put('b', 2)
        self.assertEqual(cache.get('a'), 1)
        cache.put('c', 3)
        # 'a' was accessed, so 'b' is evicted (LRU), not 'a'
        self.assertIsNone(cache.get('b'))
        self.assertIsNotNone(cache.get('a'))
        self.assertEqual(cache.size, 2)"""

content = content.replace(old_test, new_test)
p.write_text(content, encoding="utf-8")
print("Fixed LRU cache test")
