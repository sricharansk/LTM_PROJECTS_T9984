"""
ClaimSense: Synthetic Claims & Policy Dataset Generator
Generates realistic insurance claims with fraud patterns, realistic amounts, and incident narratives.
"""

import json
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

CLAIM_TYPES = [
    "Fire & Special Perils",
    "Health Mediclaim",
    "Motor Own Damage",
    "Burglary & Theft"
]

CITIES = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]

NARRATIVES = {
    "Fire & Special Perils": [
        ("Short circuit in primary electrical panel causing moderate inventory damage in warehouse B. Local fire brigade extinguished within 45 mins. Fire officer NOC submitted.", False),
        ("Stock of raw materials caught fire during night hours. Building had been unoccupied for 45 days due to renovation dispute. No watchman on duty.", True),
        ("Lightning strike damaged rooftop solar installation and ancillary equipment during heavy monsoon storm. Damage verified by building maintenance engineer.", False),
        ("Spontaneous heating and fermentation observed in stored agricultural grain bags causing internal smouldering and destruction of 50 bags.", True)
    ],
    "Health Mediclaim": [
        ("Emergency hospitalization for acute appendicitis requiring laparoscopic appendectomy. Patient admitted for 3 days at Apollo Hospital.", False),
        ("Hospitalization for severe chest pain and breathlessness 8 days after policy inception. Discharge summary indicates chronic hypertensive heart disease history of 4 years.", True),
        ("Admission for dengue fever with severe thrombocytopenia requiring platelet transfusion and 4 days ICU care.", False),
        ("Treatment for multiple contusions and minor head injury following late-night road accident. Treating physician notes acute alcohol intoxication at triage.", True)
    ],
    "Motor Own Damage": [
        ("Vehicle bumper and headlight damaged while reversing into parking pillar. GD entry made at local police station.", False),
        ("Frontal collision on expressway during dense fog. Other vehicle fled the scene. Driver was friend of insured with suspended driving license.", True),
        ("Windshield cracked due to flying gravel from a truck on state highway. Vehicle inspected by authorized service workshop.", False),
        ("Reported total loss by fire while vehicle parked on roadside late night. Forensic report indicates traces of accelerant and mismatch with battery wiring.", True)
    ],
    "Burglary & Theft": [
        ("Rear window grill forcibly cut open during holiday weekend. Laptop, cash drawer, and tools stolen. Police FIR filed within 4 hours.", False),
        ("Theft of expensive copper coils from factory store. No sign of violent or forcible entry; warehouse key found in locker and junior storekeeper absconding.", True),
        ("Break-in through broken skylight glass. Store inventory and office electronics stolen. CCTV footage showing two masked perpetrators submitted.", False)
    ]
}


def generate_synthetic_claims(count: int = 1500) -> List[Dict[str, Any]]:
    claims = []
    base_date = datetime(2025, 1, 1)

    for i in range(1, count + 1):
        claim_type = random.choice(CLAIM_TYPES)
        narrative_pair = random.choice(NARRATIVES[claim_type])
        incident_desc, is_fraud_prone = narrative_pair

        policy_start = base_date + timedelta(days=random.randint(0, 365))
        
        if is_fraud_prone:
            # Short gap between policy start and incident
            days_gap = random.randint(3, 40)
            sum_insured = random.choice([300000, 500000, 1000000, 2000000])
            claim_amount = round(sum_insured * random.uniform(0.75, 0.98), -2)
            prior_claims = random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.25, 0.15, 0.1])[0]
        else:
            days_gap = random.randint(45, 300)
            sum_insured = random.choice([500000, 1000000, 1500000, 2500000, 5000000])
            claim_amount = round(sum_insured * random.uniform(0.05, 0.45), -2)
            prior_claims = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]

        incident_date = policy_start + timedelta(days=days_gap)

        claim_id = f"CLM-2026-{10000 + i}"
        policy_num = f"POL-{claim_type[:3].upper()}-{20000 + i}"
        policy_holder = f"Insured_Party_{i}"

        claims.append({
            "claim_id": claim_id,
            "policy_number": policy_num,
            "policy_holder_name": policy_holder,
            "claim_type": claim_type,
            "claim_amount": claim_amount,
            "sum_insured": sum_insured,
            "policy_start_date": policy_start.strftime("%Y-%m-%d"),
            "incident_date": incident_date.strftime("%Y-%m-%d"),
            "incident_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
            "incident_location": random.choice(CITIES),
            "prior_claims_count": prior_claims,
            "incident_description": incident_desc,
            "is_synthetic_fraud_target": is_fraud_prone
        })

    return claims


def save_dataset():
    sample_dir = Path(__file__).resolve().parent.parent.parent / "data" / "sample"
    sample_dir.mkdir(parents=True, exist_ok=True)

    claims = generate_synthetic_claims(count=1500)

    # Save JSON
    json_path = sample_dir / "synthetic_claims.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(claims, f, indent=2)

    # Save CSV
    csv_path = sample_dir / "synthetic_claims.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=claims[0].keys())
        writer.writeheader()
        writer.writerows(claims)

    print(f"Generated {len(claims)} synthetic insurance claims.")
    print(f"Saved to: {json_path}")
    print(f"Saved to: {csv_path}")


if __name__ == "__main__":
    save_dataset()
