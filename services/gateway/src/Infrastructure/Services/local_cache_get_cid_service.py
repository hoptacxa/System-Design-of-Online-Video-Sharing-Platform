from .singleton_metadata import SingletonMeta
class LocalCacheGetCidService(metaclass=SingletonMeta):
    def __init__(self):
        self._cache = {}

    def get_by_name(self, name: str) -> str | None:
        """
        Retrieve a CID from the cache by its name.
        
        :param name: The name of the resource.
        :return: The CID if found in the cache, otherwise None.
        """
        return self._cache.get(name)

    def set(self, name: str, cid: str) -> None:
        """
        Store a CID in the cache by its name.
        
        :param name: The name of the resource.
        :param cid: The CID to associate with the resource.
        """
        self._cache[name] = cid

    def clear(self) -> None:
        """
        Clear the entire cache.
        """
        self._cache.clear()

    def delete(self, name: str) -> None:
        """
        Remove a specific entry from the cache.
        
        :param name: The name of the resource to remove.
        """
        if name in self._cache:
            del self._cache[name]
