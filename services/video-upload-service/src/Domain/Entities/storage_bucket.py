from dataclasses import dataclass

@dataclass
class StorageBucket:
    id: int
    name: str
    region: str
