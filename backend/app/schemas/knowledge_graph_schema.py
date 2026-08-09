from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class GraphNodeType(str, Enum):
    MEDICINE = "MEDICINE"
    INGREDIENT = "INGREDIENT"
    DISEASE = "DISEASE"
    SYMPTOM = "SYMPTOM"
    INTERACTION = "INTERACTION"
    SIDE_EFFECT = "SIDE_EFFECT"

class GraphEdgeType(str, Enum):
    CONTAINS_INGREDIENT = "CONTAINS_INGREDIENT"
    INDICATED_FOR_DISEASE = "INDICATED_FOR_DISEASE"
    MANIFESTS_SYMPTOM = "MANIFESTS_SYMPTOM"
    INTERACTS_WITH = "INTERACTS_WITH"
    CAUSES_SIDE_EFFECT = "CAUSES_SIDE_EFFECT"

class GraphNode(BaseModel):
    id: str
    label: str
    node_type: GraphNodeType
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    source: str
    target: str
    edge_type: GraphEdgeType
    weight: float = Field(default=1.0)
    description: str

class KnowledgeGraphRequest(BaseModel):
    query_entity: str = Field(..., json_schema_extra={"example": "Paracetamol"})
    max_depth: Optional[int] = Field(default=3, ge=1, le=5)
    include_node_types: Optional[List[GraphNodeType]] = Field(default=None)

class KnowledgeGraphResponse(BaseModel):
    entity_id: str
    entity_name: str
    entity_type: GraphNodeType
    total_nodes: int
    total_edges: int
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    graph_reasoning_paths: List[str]
    clinical_insights: List[str]
