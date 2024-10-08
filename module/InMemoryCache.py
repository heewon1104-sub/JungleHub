class InMemoryCache():

    _instance = None
    _cache_store = dict()

    def __init__(self):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def instance(classs):
        if classs._instance is None:
            classs._instance = classs.__new__(classs)
        return classs._instance

    def set(self, key, value):
        self._cache_store[key] = value

    def get(self, key):
        if key in self._cache_store:
            return self._cache_store[key]
        else:
            return None

    def delete(self, key):
        if key in self._cache_store:
            del self._cache_store[key]

inMemoryCacheInstance = InMemoryCache.instance()