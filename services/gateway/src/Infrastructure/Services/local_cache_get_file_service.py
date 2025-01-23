from .singleton_metadata import SingletonMeta
class LocalCacheGetFileService(metaclass=SingletonMeta):
    def __init__(self):
        # In-memory dictionary to store file contents
        self.cache = {}

    def add_file(self, path: str, contents: bytes) -> None:
        """
        Adds a file to the local cache.

        Args:
            path (str): The unique path of the file.
            contents (bytes): The content of the file.
        """
        self.cache[path] = contents

    def get_file_contents(self, path: str) -> bytes | None:
        """
        Retrieves file contents from the cache.

        Args:
            path (str): The unique path of the file.

        Returns:
            bytes | None: The file contents if found, or None if the file is not in the cache.
        """
        return self.cache.get(path)

    def remove_file(self, path: str) -> None:
        """
        Removes a file from the cache.

        Args:
            path (str): The unique path of the file.
        """
        if path in self.cache:
            del self.cache[path]

    def clear_cache(self) -> None:
        """
        Clears all files from the cache.
        """
        self.cache.clear()
