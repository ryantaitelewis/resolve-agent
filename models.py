from typing import Literal

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    finding: str
    source_url: str
    source_type: Literal[
        "x",
        "youtube",
        "company",
        "other",
    ]
    evidence: str
    confidence: float = Field(ge=0, le=1)
    appropriate_for_outreach: bool
    creepiness_score: float = Field(ge=0, le=1)


class ProspectResearch(BaseModel):
    prospect_summary: str
    professional_signals: list[EvidenceItem]
    personal_signals: list[EvidenceItem]
    company_signals: list[EvidenceItem]
    caveats: list[str]


class OutreachOption(BaseModel):
    name: str
    approach: Literal[
        "direct",
        "personalized",
        "fun",
    ]
    opening_hook: str
    resolve_relevance: str
    linkedin_message: str
    gift_or_activation: str | None
    why_it_might_work: str
    risks: list[str]

    relevance_score: float = Field(ge=0, le=1)
    relevance_reason: str

    creepiness_score: float = Field(ge=0, le=1)
    creepiness_reason: str


class OutreachRecommendation(BaseModel):
    recommended_option_name: str
    recommendation_reason: str
    options: list[OutreachOption]
    overall_notes: list[str]