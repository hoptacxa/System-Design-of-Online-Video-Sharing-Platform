from dataclasses import dataclass

@dataclass(frozen=True)
class Duration:
    value: int  # Duration in seconds

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Duration must be a positive integer.")
