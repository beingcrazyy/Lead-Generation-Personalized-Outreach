# Module/web_scraping.py
import re
import time
import logging
from typing import Dict, Any, Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# init OpenAI client once
client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch HTML content from a URL."""
    headers = {
        "User-Agent": "LeadGenBot/1.0 (+your_email@example.com)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        time.sleep(1.5)  # polite delay
        return resp.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


def extract_text_and_contacts(html: str) -> Dict[str, Any]:
    """Extract visible text, meta description, and contact info from HTML."""
    soup = BeautifulSoup(html, "lxml")

    # Meta description
    meta_desc = ""
    if soup.find("meta", attrs={"name": "description"}):
        meta_desc = soup.find("meta", attrs={"name": "description"}).get("content", "")

    # Grab visible paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text_blob = meta_desc + "\n" + "\n".join(paragraphs[:20])  # limit to first 20 paragraphs for brevity

    # Contact info (phone, email)
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}", html)
    phones = re.findall(r"\\+?\\d[\\d\\-\\s]{6,}\\d", html)

    # News/updates: crude search for sections with 'news' or 'updates'
    news_sections = []
    for section in soup.find_all(["section", "div"], string=re.compile(r"news|update", re.I)):
        news_sections.append(section.get_text(strip=True))

    return {
        "meta_description": meta_desc,
        "main_text": text_blob,
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "news_updates": news_sections[:3],  # only top 3
    }


def generate_key_points_with_ai(company_name: str, extracted: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send extracted text to OpenAI to generate 2–3 key points about the business,
    including contact info if found.
    """
    if not OPENAI_API_KEY:
        logger.warning("No OpenAI key found, returning stubbed key points.")
        return {
            "key_points": [
                "Example key point 1 about the business",
                "Example key point 2 about the business",
                "Example key point 3 about the business"
            ]
        }

    # Build the prompt
    text_summary = extracted.get("meta_description", "") + "\n" + extracted.get("main_text", "")
    contact_info = ""
    if extracted.get("emails") or extracted.get("phones"):
        contact_info = f"Contact info found: emails={extracted.get('emails')}, phones={extracted.get('phones')}."

    news = ""
    if extracted.get("news_updates"):
        news = f"Recent updates/news: {extracted.get('news_updates')}."

    prompt = f"""
    Given the following extracted information from {company_name}'s website:

    {text_summary}

    {contact_info}
    {news}

    Write 2-3 concise bullet points summarizing what the company does and any notable recent updates.
    Include the contact information at the end if available.
    Output only the bullet points.
    """

    logger.debug(f"Sending prompt to OpenAI for {company_name}...")

    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # or 'gpt-4o' depending on your plan
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = resp.choices[0].message.content.strip()
    key_points = [line.strip("•- ") for line in content.splitlines() if line.strip()]

    return {"key_points": key_points}


def scrape_website_and_summarize(url: str, company_name: str) -> Dict[str, Any]:
    """
    High-level function:
    - Fetch HTML
    - Extract text + contacts + news
    - Generate key points with AI
    """
    html = fetch_html(url)
    if not html:
        return {"error": f"Could not fetch {url}"}

    extracted = extract_text_and_contacts(html)
    summary = generate_key_points_with_ai(company_name, extracted)

    return {
        "company_name": company_name,
        "url": url,
        "extracted": extracted,
        "summary": summary,
    }


# result = scrape_website_and_summarize("http://www.applicantz.com", "Applicantz")
# print(result["summary"]["key_points"])