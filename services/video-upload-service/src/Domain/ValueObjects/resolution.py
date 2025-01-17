from dataclasses import dataclass

@dataclass(frozen=True)
class Resolution:
    value: str  # e.g., "1080p", "4K"

    def __post_init__(self):
        valid_resolutions = ["480p", "720p", "1080p", "1440p", "4K"]
        if self.value not in valid_resolutions:
            raise ValueError(f"Invalid resolution: {self.value}. Must be one of {valid_resolutions}.")