
class Description:
    def __init__(self, value: str):
        if len(value) > 5000:  # Example limit
            raise ValueError("Description cannot exceed 5000 characters.")
        self._value = value.strip()

    @property
    def value(self):
        return self._value

    def truncate(self, length: int) -> str:
        return self._value[:length] + ("..." if len(self._value) > length else "")

    def __str__(self):
        return self._value