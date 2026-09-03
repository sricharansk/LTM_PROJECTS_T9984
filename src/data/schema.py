"""
ClaimSense: Pydantic Data Models & Schemas
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ClaimType(str, Enum):
    FIRE_SPECIAL_PERILS = "Fire & Special Perils"
    HEALTH_MEDICLAIM = "Health Mediclaim"
    MOTOR_OWN_DAMAGE = "Motor Own Damage"
    BURGLARY_THEFT = "Burglary & Theft"
    ENGINEERING_MACHINERY = "Engineering & Machinery Breakdown"


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Recommendation(str, Enum):
    APPROVE = "Approve"
    INVESTIGATE = "Flag for Investigation"
    DENY = "Deny"


class PolicyClause(BaseModel):
    clause_id: str
    policy_type: str
    section: str
    title: str
    content: str
    relevance_score: float = 0.0
    is_exclusion: bool = False


class ClaimInput(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier")
    policy_number: str
    policy_holder_name: str
    claim_type: ClaimType
    claim_amount: float = Field(..., ge=0)
    sum_insured: float = Field(..., ge=0)
    policy_start_date: str
    incident_date: str
    incident_time: str
    incident_location: str
    prior_claims_count: int = Field(0, ge=0)
    incident_description: str = Field(..., min_length=10)


class RiskFactor(BaseModel):
    factor_name: str
    impact_score: float
    description: str


class AdjudicationResponse(BaseModel):
    claim_id: str
    adjudication_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    recommendation: Recommendation
    fraud_risk_level: RiskLevel
    fraud_risk_score: float = Field(..., ge=0.0, le=100.0)
    claim_to_sum_insured_ratio: float
    days_since_policy_start: int
    risk_factors: List[RiskFactor] = []
    cited_clauses: List[PolicyClause] = []
    adjudication_rationale: str
    investigation_action_items: List[str] = []
