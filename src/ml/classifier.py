"""
ClaimSense: Fraud & Anomaly Risk Classification Engine
"""

from typing import Tuple, List, Dict, Any
from datetime import datetime
from src.data.schema import ClaimInput, RiskLevel, RiskFactor


class FraudRiskClassifier:
    """
    Multi-factor risk assessment model for insurance claim anomaly and fraud detection.
    Combines structured feature engineering with text anomaly pattern recognition.
    """

    SUSPICIOUS_KEYWORDS = {
        "unattended": 12.0,
        "cash": 10.0,
        "delayed": 14.0,
        "no fir": 18.0,
        "no police": 15.0,
        "friend driving": 12.0,
        "unlicensed": 25.0,
        "alcohol": 30.0,
        "intoxicated": 30.0,
        "vacant": 15.0,
        "unoccupied": 15.0,
        "mismatch": 12.0,
        "late night": 8.0,
        "second time this month": 20.0,
        "total loss": 10.0
    }

    def _calculate_days_diff(self, start_date_str: str, incident_date_str: str) -> int:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            inc_date = datetime.strptime(incident_date_str, "%Y-%m-%d")
            diff = (inc_date - start_date).days
            return max(0, diff)
        except Exception:
            return 90

    def assess_risk(self, claim: ClaimInput) -> Tuple[float, RiskLevel, List[RiskFactor]]:
        risk_score = 10.0  # baseline
        risk_factors: List[RiskFactor] = []

        # 1. Claim Amount vs Sum Insured Ratio
        ratio = claim.claim_amount / max(1.0, claim.sum_insured)
        if ratio >= 0.90:
            score_delta = 28.0
            risk_score += score_delta
            risk_factors.append(RiskFactor(
                factor_name="High Sum-Insured Utilization",
                impact_score=score_delta,
                description=f"Claim amount represents {round(ratio * 100, 1)}% of total sum insured (>= 90%)."
            ))
        elif ratio >= 0.70:
            score_delta = 16.0
            risk_score += score_delta
            risk_factors.append(RiskFactor(
                factor_name="Moderate Sum-Insured Utilization",
                impact_score=score_delta,
                description=f"Claim amount represents {round(ratio * 100, 1)}% of total sum insured (>= 70%)."
            ))

        # 2. Inception Proximity (Early Claim Anomaly)
        days_active = self._calculate_days_diff(claim.policy_start_date, claim.incident_date)
        if days_active <= 15:
            score_delta = 32.0
            risk_score += score_delta
            risk_factors.append(RiskFactor(
                factor_name="Critical Inception Proximity",
                impact_score=score_delta,
                description=f"Incident occurred only {days_active} days after policy inception (<= 15 days)."
            ))
        elif days_active <= 30:
            score_delta = 20.0
            risk_score += score_delta
            risk_factors.append(RiskFactor(
                factor_name="Waiting Period Borderline",
                impact_score=score_delta,
                description=f"Incident occurred within initial 30 days ({days_active} days post-inception)."
            ))

        # 3. Prior Claim Frequency
        if claim.prior_claims_count >= 3:
            score_delta = 22.0
            risk_score += score_delta
            risk_factors.append(RiskFactor(
                factor_name="Frequent Claimant History",
                impact_score=score_delta,
                description=f"Policyholder has lodged {claim.prior_claims_count} prior claims within policy period."
            ))
        elif claim.prior_claims_count >= 2:
            score_delta = 12.0
            risk_score += score_delta
            risk_factors.append(RiskFactor(
                factor_name="Repeat Claimant",
                impact_score=score_delta,
                description=f"Policyholder has lodged {claim.prior_claims_count} prior claims."
            ))

        # 4. Text Sentiment & Suspicious Keywords
        desc_lower = claim.incident_description.lower()
        found_keywords = []
        for kw, kw_weight in self.SUSPICIOUS_KEYWORDS.items():
            if kw in desc_lower:
                found_keywords.append(kw)
                risk_score += kw_weight

        if found_keywords:
            risk_factors.append(RiskFactor(
                factor_name="Suspicious Incident Narrative Signals",
                impact_score=min(30.0, float(len(found_keywords) * 12)),
                description=f"Identified anomaly trigger keywords in narrative: {', '.join(found_keywords)}."
            ))

        # Normalize score
        final_score = min(100.0, max(5.0, round(risk_score, 1)))

        if final_score >= 65.0:
            level = RiskLevel.HIGH
        elif final_score >= 35.0:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return final_score, level, risk_factors
