# Module/data_export.py
import csv
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def save_to_csv(filename: str, companies_data: List[Dict[str, str]]) -> None:
    """
    Save a list of company data dictionaries to a CSV file.

    Each dict should contain:
    - id (company name or unique id)
    - company_name
    - website
    - linkedin_url
    - twitter_url
    - phone_number
    - description (AI-generated summary)
    - outreach_subject
    - outreach_body
    """
    if not companies_data:
        logger.warning("No company data provided to save_to_csv.")
        return

    fieldnames = [
        "id",
        "company_name",
        "website",
        "linkedin_url",
        "twitter_url",
        "phone_number",
        "description",
        "outreach_subject",
        "outreach_body",
    ]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in companies_data:
                writer.writerow({
                    "id": row.get("id") or row.get("company_name"),
                    "company_name": row.get("company_name", ""),
                    "website": row.get("website", ""),
                    "linkedin_url": row.get("linkedin_url", ""),
                    "twitter_url": row.get("twitter_url", ""),
                    "phone_number": row.get("phone_number", ""),
                    "description": row.get("description", ""),
                    "outreach_subject": row.get("outreach_subject", ""),
                    "outreach_body": row.get("outreach_body", ""),
                })
        logger.info(f"Data saved to {filename} successfully.")
    except Exception as e:
        logger.error(f"Error saving data to CSV: {e}")
