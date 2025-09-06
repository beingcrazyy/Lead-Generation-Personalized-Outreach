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
