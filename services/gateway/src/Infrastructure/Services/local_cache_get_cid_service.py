from typing import Optional
import threading

class LocalCacheGetCidService:
    def __init__(self):
        # Initialize a thread-safe dictionary to store the cache.
        self._cache = {}
        self._lock = threading.Lock()  # Ensures thread-safe operations on the cache.

    def get_by_name(self, name: str) -> Optional[str]:
        """
        Retrieve a CID from the cache by its name.
        
        :param name: The name of the resource.
        :return: The CID if found in the cache, otherwise None.
        """
        with self._lock:  # Ensure thread safety during the read operation.
            return self._cache.get(name)

    def set(self, name: str, cid: str) -> None:
        """
        Store a CID in the cache by its name.
        
        :param name: The name of the resource.
        :param cid: The CID to associate with the resource.
        """
        with self._lock:  # Ensure thread safety during the write operation.
            self._cache[name] = cid

    def clear(self) -> None:
        """
        Clear the entire cache.
        """
        with self._lock:  # Ensure thread safety during the clear operation.
            self._cache.clear()

    def delete(self, name: str) -> None:
        """
        Remove a specific entry from the cache.
        
        :param name: The name of the resource to remove.
        """
        with self._lock:  # Ensure thread safety during the delete operation.
            if name in self._cache:
                del self._cache[name]