# LeadGen Automation

This is a Python-based automation tool for **B2B lead generation**.  
It uses the Apollo API to find companies, scrapes their websites for key information,
generates 2–3 AI-powered summary points, and then produces **personalized outreach emails**
as if written by the founder of a hardware/computer store.  
Finally, it saves all results into a CSV file.

---

## Features

- 🔎 **Company Search:** Fetch companies from Apollo by keyword, size, location, limit.  
- 🌐 **Website Scraping:** Lightweight HTML fetcher + BeautifulSoup parser extracts:
  - meta description & key text
  - contact info (emails, phones)
  - news/updates if present  
- 🤖 **AI Summaries & Outreach:** Uses OpenAI GPT-4o-mini to:
  - create 2–3 key bullet points summarizing the company
  - generate a professional B2B outreach email (subject + body)  
- 📑 **CSV Export:** Saves all enriched leads to `final_leads.csv`.  
- ⚠️ **Robustness:** Logs each step; skips gracefully if data missing or APIs fail.  

---

## Requirements

- Python 3.9+
- A free Apollo account for API key (or use mock data)
- An OpenAI API key

Install dependencies:

```bash
pip install -r requirements.txt
```




Setup

Clone this repo or copy the code into your project folder.

Create a .env file in the project root with your API keys:

```bash
APOLLO_API_KEY=your_apollo_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Make sure your folder structure looks like:

LeadGen_Automation/
├─ main.py
├─ Module/
│  ├─ apollo_integration.py
│  ├─ web_scraping.py
│  ├─ outreach_generator.py
│  ├─ data_export.py
├─ requirements.txt
├─ README.md
└─ .env

Usage

Run the script:

```bash
python main.py
```

You’ll be prompted (in plain English) for:

Industry/keyword (default: software)

Company size range (default: 50-200)

Location (default: Bangalore)

Number of companies (default: 10)

Press Enter to accept defaults.

The script will:

Search Apollo for matching companies.

Scrape each website.

Generate AI summaries & outreach messages.

Save everything to final_leads.csv in the project root.

Output CSV

Each row contains:

| id | company_name | website | linkedin_url | twitter_url | phone_number | description | outreach_subject | outreach_body |

Logs

The script logs INFO messages for progress and ERROR messages for problems.
Check the console output to monitor each step.

Notes

If Apollo API fails (rate limits, free tier limits), you can plug in your own mock data in apollo_integration.py to keep the pipeline working.

If the OpenAI API key is missing, the script returns stub summaries and outreach messages for testing.
