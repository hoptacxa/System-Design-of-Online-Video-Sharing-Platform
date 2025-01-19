import re

class Cid:
    """
    Represents a Content Identifier (CID) for IPFS.

    Attributes:
        value (str): The string representation of the CID.
    """
    _CID_REGEX = r"^Qm[1-9A-Za-z]{44}$"  # Example: Basic validation for CIDv0 (Qm... format)

    def __init__(self, value: str):
        """
        Initializes a new instance of the Cid class.

        Args:
            value (str): The string representation of the CID.

        Raises:
            ValueError: If the CID is not valid.
        """
        if not self._is_valid_cid(value):
            raise ValueError(f"Invalid IPFS CID: {value}")
        self.value = value

    @staticmethod
    def _is_valid_cid(value: str) -> bool:
        """
        Validates the given CID string.

        Args:
            value (str): The CID string to validate.

        Returns:
            bool: True if the CID is valid, otherwise False.
        """
        return bool(re.match(Cid._CID_REGEX, value))

    def __str__(self) -> str:
        """
        Returns the string representation of the CID.

        Returns:
            str: The CID as a string.
        """
        return self.value

    def __eq__(self, other) -> bool:
        """
        Checks equality with another Cid object.

        Args:
            other (Cid): The other Cid object to compare.

        Returns:
            bool: True if the CIDs are equal, otherwise False.
        """
        if isinstance(other, Cid):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        """
        Returns the hash value of the CID.

        Returns:
            int: The hash value of the CID.
        """
        return hash(self.value)
