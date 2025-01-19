from typing import List, Optional
from Domain.ValueObjects.cid import Cid

class NodeReadRepository:
    def __init__(self):
        self._nodes = [
            {
                "uuid": "1",
                "routing_table": [],
            }
        ]
    def get_node_by_cid(self, cid: Cid) -> dict:
        return self._nodes[0]
