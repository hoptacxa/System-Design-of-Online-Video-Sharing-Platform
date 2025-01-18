class Title:
    def __init__(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty.")
        if len(value) > 255:
            raise ValueError("Title cannot exceed 255 characters.")
        self._value = value.strip()

    @property
    def value(self):
        return self._value