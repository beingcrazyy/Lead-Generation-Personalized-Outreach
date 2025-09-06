# Module/outreach_generator.py
import os
import logging
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_outreach(company_name: str, description: str) -> Dict[str, str]:
    """
    Generate a personalized outreach message using OpenAI.
    Returns a dict with 'subject' and 'body'.
    """
    if not OPENAI_API_KEY:
        logger.warning("No OpenAI key found, returning stubbed outreach message.")
        return {
            "subject": f"Introduction to our solutions for {company_name}",
            "body": f"Hello Team {company_name},\n\nWe wanted to introduce our solutions..."
        }

    prompt = f"""
    You are the founder of a hardware and computer solutions store.
    You are reaching out to a new business client (company) to offer personalized
    hardware/computer solutions that fit their specific needs.

    Company Name: {company_name}
    Company Description: {description}

    Write a concise, professional B2B outreach email addressed to the company (we don't have a person's name).
    Make it clear you are the founder of a hardware/computer solutions store.
    Highlight how your hardware or computer solutions can benefit their business given the context.
    Return only a JSON object with two keys:
    - subject: A short, catchy subject line
    - body: The email body in professional tone

    Example output:
    {{"subject": "...", "body": "..."}}

    My name : Priyanshu Khandelwal
    Company Name : LeadGenie    
    My role : Founder & CEO
    My email : p.khandelwal@leadgenie.com
    """

    logger.debug(f"Sending outreach prompt to OpenAI for {company_name}...")

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    content = resp.choices[0].message.content.strip()
    # attempt to parse JSON safely
    import json
    try:
        result = json.loads(content)
        subject = result.get("subject", "").strip()
        body = result.get("body", "").strip()
    except json.JSONDecodeError:
        # fallback: treat content as plain text
        logger.warning("Could not parse JSON from OpenAI, returning raw text.")
        subject = f"Introducing our solutions for {company_name}"
        body = content

    return {"subject": subject, "body": body}


# desc = "A SaaS company providing AI-driven analytics for e-commerce businesses."
# msg = generate_outreach("Acme Analytics", desc)
# print("Subject:", msg["subject"])
# print("Body:\n", msg["body"])