import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from models import ProspectResearch, OutreachRecommendation
from prompts import (
    OUTREACH_GENERATION_PROMPT,
    PROSPECT_RESEARCH_PROMPT,
)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)



def research_prospect(
    name: str,
    company: str,
    role: str = "",
    x_url: str = "",
    youtube_url: str = "",
) -> ProspectResearch:
    prospect_details = f"""
    Prospect name: {name}
    Company: {company}
    Role: {role or "Unknown"}
    X profile: {x_url or "Not supplied"}
    YouTube interview: {youtube_url or "Not supplied"}

    Research this specific person. Prioritize information that could support
    thoughtful B2B outreach for Resolve AI.
    """

    response = client.responses.parse(
        model="gpt-5-mini",
        tools=[
            {
                "type": "web_search",
                "search_context_size": "medium",
            }
        ],
        input=[
            {
                "role": "system",
                "content": PROSPECT_RESEARCH_PROMPT,
            },
            {
                "role": "user",
                "content": prospect_details,
            },
        ],
        text_format=ProspectResearch,
    )

    if response.output_parsed is None:
        raise RuntimeError("The model did not return a valid research report.")

    return response.output_parsed

def research_prospect(
    name: str,
    company: str,
    role: str = "",
    x_url: str = "",
    youtube_url: str = "",
) -> ProspectResearch:
    details = f"""
    Prospect name: {name}
    Company: {company}
    Role: {role or "Unknown"}
    Provided X URL: {x_url or "None"}
    Provided YouTube URL: {youtube_url or "None"}

    Research this exact person.

    Search specifically for:
    - recent public posts and indexed activity from X;
    - YouTube interviews, conference talks, podcasts, or panels;
    - professional comments relevant to production engineering;
    - light personal interests they publicly discussed;
    - recent company triggers relevant to Resolve AI.

    If a URL was provided, prioritize it as an identity anchor.
    """
    

    response = client.responses.parse(
        model="gpt-5-mini",
        tools=[
            {
                "type": "web_search",
                "search_context_size": "high",
            }
        ],
        input=[
            {
                "role": "system",
                "content": PROSPECT_RESEARCH_PROMPT,
            },
            {
                "role": "user",
                "content": details,
            },
        ],
        text_format=ProspectResearch,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The model did not return valid prospect research."
        )

    return response.output_parsed

def generate_outreach_options(
    name: str,
    company: str,
    role: str,
    research: ProspectResearch,
) -> OutreachRecommendation:
    payload = {
        "prospect": {
            "name": name,
            "company": company,
            "role": role,
        },
        "research": research.model_dump(),
    }

    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": OUTREACH_GENERATION_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(payload, indent=2),
            },
        ],
        text_format=OutreachRecommendation,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "The model did not return valid outreach options."
        )

    return response.output_parsed

def run_prospect_agent(
    name: str,
    company: str,
    role: str = "",
    x_url: str = "",
    youtube_url: str = "",
) -> tuple[ProspectResearch, OutreachRecommendation]:
    research = research_prospect(
        name=name,
        company=company,
        role=role,
        x_url=x_url,
        youtube_url=youtube_url,
    )

    recommendation = generate_outreach_options(
        name=name,
        company=company,
        role=role,
        research=research,
    )

    return research, recommendation