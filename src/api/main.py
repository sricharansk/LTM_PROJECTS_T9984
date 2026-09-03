"""
ClaimSense: FastAPI Adjudication & Knowledge Assistant Service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from src.data.schema import ClaimInput, AdjudicationResponse
from src.rag.chain import AdjudicationEngine
from src.rag.corpus import POLICY_CORPUS
from src.data.generate_synthetic_data import generate_synthetic_claims

app = FastAPI(
    title="ClaimSense API",
    description="RAG-Based Insurance Claims Adjudication & Policy Knowledge Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AdjudicationEngine()
_cached_claims = generate_synthetic_claims(count=50)


@app.get("/")
def root():
    return {
        "service": "ClaimSense API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": [
            "/health",
            "/api/v1/claims/adjudicate",
            "/api/v1/claims",
            "/api/v1/policies",
            "/api/v1/analytics"
        ]
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ClaimSense"}


@app.post("/api/v1/claims/adjudicate", response_model=AdjudicationResponse)
def adjudicate_claim(claim: ClaimInput):
    try:
        result = engine.adjudicate(claim)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/claims")
def list_claims(limit: int = 20):
    return {"total": len(_cached_claims), "claims": _cached_claims[:limit]}


@app.get("/api/v1/policies")
def list_policies():
    return {"total_clauses": len(POLICY_CORPUS), "clauses": POLICY_CORPUS}


@app.get("/api/v1/analytics")
def get_analytics():
    adjudicated = [engine.adjudicate(ClaimInput(**c)) for c in _cached_claims[:30]]

    recommendation_counts = {}
    risk_level_counts = {}
    clause_citations = {}

    for res in adjudicated:
        rec = res.recommendation.value
        risk = res.fraud_risk_level.value
        recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        risk_level_counts[risk] = risk_level_counts.get(risk, 0) + 1

        for c in res.cited_clauses:
            clause_citations[c.clause_id] = clause_citations.get(c.clause_id, 0) + 1

    return {
        "total_claims_sampled": len(adjudicated),
        "recommendation_distribution": recommendation_counts,
        "risk_level_distribution": risk_level_counts,
        "top_cited_clauses": sorted(clause_citations.items(), key=lambda x: x[1], reverse=True)[:5]
    }
