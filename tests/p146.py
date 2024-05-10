from resounds import completions

class LRUCache:
    """LRUCache (最近最少使用) 缓存约束的数据结构。"""

    def __init__(self, capacity: int):
        """以 正整数 作为容量 capacity 初始化 LRU 缓存"""
        ...

    def get(self, key: int) -> int:
        """如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。"""
        ...

    def put(self, key: int, value: int) -> None:
        """如果关键字 key 已经存在，则变更其数据值 value ；如果不存在，则向缓存中插入该组 key-value 。如果插入操作导致关键字数量超过 capacity ，则应该逐出最久未使用的关键字。"""
        ...

code = completions(LRUCache)
print('-' * 8)
print(code)
print('-' * 8)
exec(code)

if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1,1)
    cache.put(2,2)
    print(cache.get(1))
    cache.put(3,3)
    print(cache.get(2))
    cache.put(4,4)
    print(cache.get(1))
    print(cache.get(3))
    print(cache.get(4))
