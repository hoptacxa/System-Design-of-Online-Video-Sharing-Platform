class FileKey:
    """
    Represents a file key as a value object, ensuring validation and immutability.
    """
    def __init__(self, key: str):
        if not key or not isinstance(key, str):
            raise ValueError("FileKey must be a non-empty string.")
        self._key = key

    @property
    def key(self) -> str:
        """
        Returns the file key as a string.
        """
        return self._key

    def __str__(self) -> str:
        """
        String representation of the FileKey.
        """
        return self._key

    def __eq__(self, other) -> bool:
        """
        Compares two FileKey objects for equality based on the key value.
        """
        return isinstance(other, FileKey) and self._key == other._key

    def __hash__(self) -> int:
        """
        Allows the FileKey to be used in hashed collections like sets and dictionaries.
        """
        return hash(self._key)
