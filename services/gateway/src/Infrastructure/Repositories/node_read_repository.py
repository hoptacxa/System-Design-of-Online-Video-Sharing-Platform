from typing import List, Optional
from Domain.ValueObjects.cid import Cid

class NodeReadRepository:
    def get_node_by_cid(self, cid: Cid) -> Optional[dict]:
        raise NotImplementedError
