# main.py
import logging
from Module.apollo_integration import search_companies
from Module.web_scraping import scrape_website_and_summarize
from Module.AI_message_generation import generate_outreach
from Module.utils import save_to_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def prompt_user_parameters():
    """Prompt user for search parameters with defaults."""
    print("Welcome to the LeadGen CLI!\n")
    default_keyword = ["software"]
    default_size = ["50,200"]
    default_location = ["Bangalore"]
    default_limit = 10

    keyword = input(f"What industry/keyword? (default: {default_keyword}): ").strip() or default_keyword
    size = input(f"What company size range? (default: {default_size}): ").strip() or default_size
    location = input(f"In which location? (default: {default_location}): ").strip() or default_location
    limit_input = input(f"How many companies? (default: {default_limit}): ").strip()

    limit = default_limit
    if limit_input.isdigit():
        limit = int(limit_input)

    return {
        "keyword": keyword,
        "size": size,
        "location": location,
        "limit": limit,
    }


def main():
    params = prompt_user_parameters()
    logging.info(f"Searching companies with params: {params}")

    try:
        companies = search_companies(**params)
    except Exception as e:
        logging.error(f"Apollo API call failed: {e}")
        companies = []  # fallback
    if not companies:
        logging.warning("No companies found, exiting.")
        return

    final_data = []

    for idx, company in enumerate(companies, start=1):
        company_name = company.get("company_name", "")
        website = company.get("website", "")
        logging.info(f"[{idx}/{len(companies)}] Processing: {company_name}")

        # Scrape + summarize
        description = ""
        try:
            if website:
                scraped = scrape_website_and_summarize(website, company_name)
                if "summary" in scraped and "key_points" in scraped["summary"]:
                    description = "\n".join(scraped["summary"]["key_points"])
                else:
                    description = ""
            else:
                logging.warning(f"No website for {company_name}")
        except Exception as e:
            logging.error(f"Error scraping {company_name}: {e}")

        # Generate outreach
        outreach_subject = ""
        outreach_body = ""
        try:
            outreach = generate_outreach(company_name, description)
            outreach_subject = outreach.get("subject", "")
            outreach_body = outreach.get("body", "")
        except Exception as e:
            logging.error(f"Error generating outreach for {company_name}: {e}")

        # Merge data
        final_data.append({
            "id": company.get("id") or company_name,
            "company_name": company_name,
            "website": website,
            "linkedin_url": company.get("linkedin_url", ""),
            "twitter_url": company.get("twitter_url", ""),
            "phone_number": company.get("phone_number", ""),
            "description": description,
            "outreach_subject": outreach_subject,
            "outreach_body": outreach_body,
        })

    # Save to CSV
    save_to_csv("final_leads.csv", final_data)
    logging.info("All done! Results saved to final_leads.csv")


if __name__ == "__main__":
    main()
