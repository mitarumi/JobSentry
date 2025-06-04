from remoteok import remoteok_fetch
import schedule
import time
from email_config import send_email
import argparse
import json

def get_filters():
    parser = argparse.ArgumentParser(description="Filter jobs based on roles, location, and salary.")
    parser.add_argument("--roles", nargs="+", help="List of job roles to filter by")
    parser.add_argument("--location", nargs="+", help="Preferred job locations")
    parser.add_argument("--salary", type=int, help="Minimum salary threshold")

    args = parser.parse_args()

    try:
        with open("filters.json", "r") as filters_file:
            saved_filters = json.load(filters_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Filters file missing or corrupted. Using empty defaults.")
        saved_filters = {"roles": [], "location": [], "salary": 0}

    # Override saved filters with CLI inputs if provided
    filters = {
        "roles": args.roles if args.roles else saved_filters.get("roles", []),
        "location": args.location if args.location else saved_filters.get("location", []),
        "salary": args.salary if args.salary else saved_filters.get("salary", 0),
    }

    # **NEW FIX**: Save updated filters back to `filters.json`
    try:
        with open("filters.json", "w", encoding="utf-8") as filters_file:
            json.dump(filters, filters_file, indent=4)
        print("✅ Filters updated successfully.")
    except Exception as e:
        print(f"❌ Error saving updated filters: {e}")

    return filters

get_filters()
def run_scraper():
    scraper = remoteok_fetch()
    scraper.fetch_jobs_function()
    scraper.filter_jobs_function()
    send_email()  # Implement your email function

schedule.every().day.at("08:00").do(run_scraper)  # Runs every day at 8 AM

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
