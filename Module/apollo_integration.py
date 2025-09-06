# Module/apollo_integration.py
import os
import logging
from typing import List, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()  # load APOLLO_API_KEY from .env

APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
APOLLO_BASE_URL = "https://api.apollo.io/api/v1/organizations/search"

# Configure logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # or INFO in production


def search_companies(

    keyword: Optional[str] = ["technology", "software", "IT services"],
    size: Optional[str] = ["200,500"],
    location: Optional[str] = ["united states"],
    limit: int = 10

) -> List[Dict]:
    """
    Search companies via Apollo 'v1/organizations/search' endpoint.

    :param keyword: Industry keyword (e.g., 'software')
    :param size: Company size (e.g., '50-200')
    :param location: Optional location filter (e.g., 'Bangalore')
    :param limit: Max number of companies to return
    :return: list of dicts with company details
    """

    if not APOLLO_API_KEY:
        logger.error("Apollo API key not found. Please set APOLLO_API_KEY in .env.")
        raise RuntimeError("Apollo API key missing")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": APOLLO_API_KEY,  # Apollo requires X-Api-Key
    }

    payload = {
        "q_organization_keyword_tags": keyword,
        "page": 1,
        "per_page": limit,
    }

    if size:
        payload["organization_num_employees_ranges"] = size
    if location:
        payload["organization_locations"] = location

    logger.info(f"Searching Apollo for keyword='{keyword}', size='{size}', location='{location}', limit={limit}")
    try:
        resp = requests.post(APOLLO_BASE_URL, headers=headers, json=payload, timeout=10)
        logger.debug(f"Apollo status: {resp.status_code}, response text: {resp.text[:500]}")  # first 500 chars
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Apollo API request failed: {e}")
        raise

    data = resp.json()
    organizations = data.get("organizations", []) or data.get("data", [])  # adjust if Apollo changes keys

    results = []
    for org in organizations:
        results.append({
            "company_id": org.get("id"),
            "company_name": org.get("name"),
            "industry": org.get("industry") or keyword,
            "employee_count": org.get("estimated_num_employees"),
            "website": org.get("website_url"),
            "linkedin": org.get("linkedin_url"),
            "twitter": org.get("twitter_url"),
            "phone": org.get("sanitized_phone"),
        })

    logger.info(f"Found {len(results)} organizations from Apollo.")
    return results


# companies = search_companies()
# for c in companies:
#     print(c)