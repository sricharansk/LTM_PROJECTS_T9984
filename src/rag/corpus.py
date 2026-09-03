"""
ClaimSense: Comprehensive Policy Wording, Exclusion Clauses, and IRDAI Regulations Corpus
"""

from typing import List, Dict, Any

POLICY_CORPUS = [
    {
        "clause_id": "FSP-SEC-1.1",
        "policy_type": "Fire & Special Perils",
        "section": "Section I: Insuring Agreement",
        "title": "Coverage of Fire & Lightning Damage",
        "content": "The company agrees that if any property insured be destroyed or damaged by Fire (excluding destruction or damage caused by its own fermentation, natural heating or spontaneous combustion) or Lightning, the company will pay to the insured the value of the property at the time of the happening of its destruction or the amount of such damage.",
        "is_exclusion": False
    },
    {
        "clause_id": "FSP-EXC-4.1",
        "policy_type": "Fire & Special Perils",
        "section": "Section IV: General Exclusions",
        "title": "Spontaneous Combustion & Fermentation Exclusion",
        "content": "Loss, destruction or damage caused by own fermentation, natural heating or spontaneous combustion or by its undergoing any heating or drying process is strictly excluded from coverage unless specifically endorsed as an add-on cover.",
        "is_exclusion": True
    },
    {
        "clause_id": "FSP-EXC-4.2",
        "policy_type": "Fire & Special Perils",
        "section": "Section IV: General Exclusions",
        "title": "War, Invasion & Act of Foreign Enemy",
        "content": "Loss, destruction or damage occasioned by or through or in consequence of war, invasion, act of foreign enemy, hostilities or war-like operations (whether war be declared or not), civil war, mutiny, civil commotion, or military rising is expressly excluded.",
        "is_exclusion": True
    },
    {
        "clause_id": "FSP-EXC-4.3",
        "policy_type": "Fire & Special Perils",
        "section": "Section IV: General Exclusions",
        "title": "Unoccupied Premises Beyond 30 Days",
        "content": "If the building insured or containing the insured property becomes unoccupied and so remains for a period of more than 30 consecutive days without prior written consent and endorsement from the company, all coverage under this policy shall cease immediately.",
        "is_exclusion": True
    },
    {
        "clause_id": "FSP-COND-6.2",
        "policy_type": "Fire & Special Perils",
        "section": "Section VI: Claims Conditions",
        "title": "Immediate Notification Requirement",
        "content": "On the happening of any loss or damage, the insured shall forthwith give notice thereof to the Company within 7 days and within 15 days after the loss or damage submit in writing full particulars of the claim including books of accounts, invoices, and vouchers.",
        "is_exclusion": False
    },
    {
        "clause_id": "HLT-SEC-2.1",
        "policy_type": "Health Mediclaim",
        "section": "Section II: In-Patient Hospitalization",
        "title": "In-Patient Care & Active Medical Treatment",
        "content": "The insurer will indemnify the insured person for medical expenses incurred in respect of hospitalization for a minimum period of 24 consecutive hours for covered illness or injury, up to the sum insured specified in the policy schedule.",
        "is_exclusion": False
    },
    {
        "clause_id": "HLT-EXC-3.1",
        "policy_type": "Health Mediclaim",
        "section": "Section III: Standard Exclusions",
        "title": "Pre-Existing Diseases (PED) Waiting Period",
        "content": "Expenses related to the treatment of a Pre-Existing Disease (PED) and its direct complications shall be excluded until the expiry of 36 months of continuous coverage after the date of inception of the first policy with the insurer.",
        "is_exclusion": True
    },
    {
        "clause_id": "HLT-EXC-3.2",
        "policy_type": "Health Mediclaim",
        "section": "Section III: Standard Exclusions",
        "title": "Initial 30-Day Waiting Period",
        "content": "Expenses related to the treatment of any illness within 30 days from the first policy commencement date shall be excluded except claims arising from an accident. This exclusion ceases to apply upon continuous policy renewal.",
        "is_exclusion": True
    },
    {
        "clause_id": "HLT-EXC-3.3",
        "policy_type": "Health Mediclaim",
        "section": "Section III: Standard Exclusions",
        "title": "Cosmetic, Aesthetic & Obesity Treatment",
        "content": "Expenses incurred for cosmetic or plastic surgery or any treatment purely aesthetic in nature, as well as surgical treatment of obesity that does not satisfy morbid obesity criteria, are completely excluded.",
        "is_exclusion": True
    },
    {
        "clause_id": "HLT-EXC-3.4",
        "policy_type": "Health Mediclaim",
        "section": "Section III: Standard Exclusions",
        "title": "Substance Abuse & Alcohol Induced Conditions",
        "content": "Expenses incurred for treatment directly or indirectly arising from the use of intoxicating substances, alcohol abuse, or non-prescribed narcotics are excluded from policy indemnification.",
        "is_exclusion": True
    },
    {
        "clause_id": "MOT-SEC-1.1",
        "policy_type": "Motor Own Damage",
        "section": "Section I: Loss of or Damage to Vehicle",
        "title": "Accidental External Damage & Total Loss",
        "content": "The Company will indemnify the insured against loss or damage to the vehicle insured and its accessories by accidental external means, fire, explosion, self-ignition, lightning, burglary, housebreaking, or theft.",
        "is_exclusion": False
    },
    {
        "clause_id": "MOT-EXC-2.1",
        "policy_type": "Motor Own Damage",
        "section": "Section II: General Exclusions",
        "title": "Driving Under the Influence of Alcohol / Drugs",
        "content": "The Company shall not be liable to make any payment in respect of any accidental loss or damage suffered whilst the insured vehicle is being driven by any person whilst under the influence of intoxicating liquor or drugs.",
        "is_exclusion": True
    },
    {
        "clause_id": "MOT-EXC-2.2",
        "policy_type": "Motor Own Damage",
        "section": "Section II: General Exclusions",
        "title": "Consequential Loss & Mechanical Breakdown",
        "content": "Any accidental loss or damage resulting directly from mechanical or electrical breakdown, failure or breakage, or wear and tear, and normal depreciation is expressly excluded from coverage.",
        "is_exclusion": True
    },
    {
        "clause_id": "MOT-EXC-2.3",
        "policy_type": "Motor Own Damage",
        "section": "Section II: General Exclusions",
        "title": "Lack of Valid Driving License",
        "content": "Any accidental loss or damage suffered whilst the insured vehicle is being driven by any person other than a person holding an effective and valid driving license at the time of the accident is not admissible under the policy.",
        "is_exclusion": True
    },
    {
        "clause_id": "BUR-SEC-1.1",
        "policy_type": "Burglary & Theft",
        "section": "Section I: Scope of Cover",
        "title": "Violent & Forcible Entry Burglary",
        "content": "Indemnification against loss or damage to the property contained in the insured premises resulting from actual, forcible, and violent entry into or exit from the premises, or following assault or violence to the insured or employees.",
        "is_exclusion": False
    },
    {
        "clause_id": "BUR-EXC-3.1",
        "policy_type": "Burglary & Theft",
        "section": "Section III: Exclusions",
        "title": "Inside Job / Employee Collusion Exclusion",
        "content": "Loss or damage where any employee, business partner, family member, or domestic servant of the insured is involved as principal or accessory in the burglary or theft is expressly excluded unless specifically declared.",
        "is_exclusion": True
    },
    {
        "clause_id": "IRDAI-CIRC-2024-07",
        "policy_type": "Regulatory Guideline",
        "section": "IRDAI Protection of Policyholders' Interests Regulations",
        "title": "Mandatory Turnaround Time & Evidence Standard for Repudiation",
        "content": "No insurer shall repudiate a claim without obtaining an independent surveyor report and providing a reasoned written explanation citing the specific clause in the policy terms. Repudiation on technical delay grounds without prejudice is prohibited if genuine force majeure or valid grounds for delay exist.",
        "is_exclusion": False
    }
]
