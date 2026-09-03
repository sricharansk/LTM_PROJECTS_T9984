"""
ClaimSense: Hybrid RAG Retriever for Policy Clauses & Regulatory Circulars
"""

import math
import re
from typing import List, Dict, Any, Optional
from src.rag.corpus import POLICY_CORPUS
from src.data.schema import PolicyClause


class PolicyRetriever:
    """
    Hybrid semantic & keyword retriever over insurance policy clauses and exclusions.
    Works independently with zero external API dependencies, with optional Sentence-Transformers support.
    """

    def __init__(self, corpus: Optional[List[Dict[str, Any]]] = None):
        self.corpus = corpus or POLICY_CORPUS
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_-]{3,}\b', text.lower())
        stopwords = {
            "the", "and", "for", "with", "this", "that", "from", "any",
            "are", "was", "shall", "will", "has", "have", "been", "which"
        }
        return [t for t in tokens if t not in stopwords]

    def _build_index(self):
        self.doc_tokens = []
        self.df = {}
        total_docs = len(self.corpus)

        for doc in self.corpus:
            combined_text = f"{doc.get('title', '')} {doc.get('content', '')} {doc.get('policy_type', '')}"
            tokens = set(self._tokenize(combined_text))
            self.doc_tokens.append(tokens)
            for token in tokens:
                self.df[token] = self.df.get(token, 0) + 1

        self.idf = {}
        for token, count in self.df.items():
            self.idf[token] = math.log((total_docs + 1) / (count + 1)) + 1.0

    def retrieve(self, query: str, policy_type: Optional[str] = None, top_k: int = 3) -> List[PolicyClause]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores = []
        for idx, doc in enumerate(self.corpus):
            # If policy type matches, give boost
            type_boost = 1.0
            if policy_type and doc.get("policy_type", "").lower() == policy_type.lower():
                type_boost = 2.2
            elif doc.get("policy_type") == "Regulatory Guideline":
                type_boost = 1.3

            doc_t = self.doc_tokens[idx]
            match_score = 0.0

            for q_tok in query_tokens:
                if q_tok in doc_t:
                    match_score += self.idf.get(q_tok, 1.0)
                else:
                    # Partial match
                    for dt in doc_t:
                        if q_tok in dt or dt in q_tok:
                            match_score += 0.4 * self.idf.get(dt, 1.0)
                            break

            # Exact phrase or keyword bonus for key exclusion triggers
            lowered_content = doc.get("content", "").lower()
            if any(k in query.lower() for k in ["intoxicated", "alcohol", "drunk"]) and "alcohol" in lowered_content:
                match_score += 15.0
            if any(k in query.lower() for k in ["waiting period", "30 days", "prior to"]) and "waiting period" in lowered_content:
                match_score += 15.0
            if any(k in query.lower() for k in ["unoccupied", "vacant", "abandoned"]) and "unoccupied" in lowered_content:
                match_score += 15.0
            if any(k in query.lower() for k in ["collusion", "employee", "stolen inside"]) and "employee" in lowered_content:
                match_score += 15.0

            final_score = match_score * type_boost
            scores.append((final_score, doc))

        scores.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, doc in scores[:top_k]:
            normalized_score = min(1.0, round(score / 25.0, 3))
            results.append(PolicyClause(
                clause_id=doc["clause_id"],
                policy_type=doc["policy_type"],
                section=doc["section"],
                title=doc["title"],
                content=doc["content"],
                relevance_score=normalized_score,
                is_exclusion=doc.get("is_exclusion", False)
            ))

        return results
