"""
ClaimSense: End-to-End Adjudication Decision & Clause Citation Engine
"""

from typing import List
from datetime import datetime
from src.data.schema import (
    ClaimInput,
    AdjudicationResponse,
    Recommendation,
    RiskLevel,
    PolicyClause
)
from src.ml.classifier import FraudRiskClassifier
from src.rag.retriever import PolicyRetriever


class AdjudicationEngine:
    """
    Combines hybrid RAG clause retrieval with multi-factor ML anomaly scoring
    to output citation-backed claim adjudication recommendations.
    """

    def __init__(self):
        self.classifier = FraudRiskClassifier()
        self.retriever = PolicyRetriever()

    def adjudicate(self, claim: ClaimInput) -> AdjudicationResponse:
        # 1. Assess fraud and anomaly risk
        risk_score, risk_level, risk_factors = self.classifier.assess_risk(claim)

        # 2. Retrieve relevant policy clauses
        search_query = f"{claim.claim_type.value} {claim.incident_description}"
        retrieved_clauses = self.retriever.retrieve(
            query=search_query,
            policy_type=claim.claim_type.value,
            top_k=3
        )

        # 3. Determine Adjudication Recommendation
        # Check if an active exclusion clause was triggered
        has_triggered_exclusion = any(
            c.is_exclusion and c.relevance_score >= 0.50
            for c in retrieved_clauses
        )

        claim_ratio = claim.claim_amount / max(1.0, claim.sum_insured)
        days_active = self.classifier._calculate_days_diff(claim.policy_start_date, claim.incident_date)

        action_items: List[str] = []

        if has_triggered_exclusion:
            recommendation = Recommendation.DENY
            triggered = [c for c in retrieved_clauses if c.is_exclusion and c.relevance_score >= 0.50][0]
            rationale = (
                f"Claim is recommended for DENIAL pursuant to exclusion clause {triggered.clause_id} "
                f"('{triggered.title}'). The incident circumstances described directly align with non-indemnifiable "
                f"conditions stipulated in {triggered.section} of the policy wording."
            )
            action_items.append(f"Issue formal Notice of Repudiation citing clause {triggered.clause_id}.")
            action_items.append("Attach independent assessment report adhering to IRDAI Protection of Policyholders' Interests regulations.")

        elif risk_level == RiskLevel.HIGH:
            recommendation = Recommendation.INVESTIGATE
            rationale = (
                f"Claim flagged for IN-DEPTH INVESTIGATION due to High Anomaly Score ({risk_score}/100). "
                f"Key concerns: Claim utilizes {round(claim_ratio*100, 1)}% of sum insured within {days_active} days "
                f"of policy inception, coupled with multiple anomaly flags in incident narrative."
            )
            action_items.append("Assign Senior Forensic Loss Adjuster for physical site inspection.")
            action_items.append("Request verified bank statement, books of accounts, and official police/GD entry records.")
            action_items.append("Verify pre-existing condition timeline with treating hospital registry.")

        elif risk_level == RiskLevel.MEDIUM:
            recommendation = Recommendation.INVESTIGATE
            rationale = (
                f"Claim routed for SECONDARY REVIEW with Moderate Anomaly Score ({risk_score}/100). "
                f"Standard document verification required before settlement authorization."
            )
            action_items.append("Request original bills, diagnostic reports, and discharge summary.")
            action_items.append("Cross-reference historical claim frequency with central insurance bureau.")

        else:
            recommendation = Recommendation.APPROVE
            primary_clause = retrieved_clauses[0] if retrieved_clauses else None
            clause_ref = f" under {primary_clause.clause_id} ('{primary_clause.title}')" if primary_clause else ""
            rationale = (
                f"Claim recommended for APPROVAL{clause_ref}. Incident falls squarely within policy insuring agreements. "
                f"Low anomaly risk score ({risk_score}/100) and no statutory exclusions triggered."
            )
            action_items.append("Proceed with automated claim settlement voucher generation.")
            action_items.append("Notify policyholder via SMS/Email regarding approved indemnity amount.")

        return AdjudicationResponse(
            claim_id=claim.claim_id,
            adjudication_timestamp=datetime.now().isoformat(),
            recommendation=recommendation,
            fraud_risk_level=risk_level,
            fraud_risk_score=risk_score,
            claim_to_sum_insured_ratio=round(claim_ratio, 4),
            days_since_policy_start=days_active,
            risk_factors=risk_factors,
            cited_clauses=retrieved_clauses,
            adjudication_rationale=rationale,
            investigation_action_items=action_items
        )
