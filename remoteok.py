from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import re
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
class remoteok_fetch():
    def __init__(self):
        self.driver = self.get_driver()
        self.jobs = []

    def get_driver(self):
        try:
            options = ChromeOptions()
            options.add_argument("--headless")  # Enable headless mode for Chrome
            options.add_argument("--disable-gpu")  # Improves performance on some systems
            options.add_argument("--log-level=3")  # Suppresses warnings
            driver = webdriver.Chrome(options=options)
            print("✅ Using ChromeDriver in headless mode")
        except Exception as e:
            print(f"⚠️ ChromeDriver failed: {e}\nAttempting EdgeDriver...")
            try:            
                edge_options = Options()
                edge_options.add_argument("--headless")  # Enable headless mode for Edge
                edge_options.add_argument("--disable-gpu")
                driver = webdriver.Edge(options=edge_options)
                print("✅ Using EdgeDriver in headless mode")
            except Exception as e:
                print(f"❌ EdgeDriver also failed: {e}\nExiting program.")
                exit()
        return driver

    def fetch_jobs_function(self):
        try:
            self.driver.get("https://remoteok.com/")  # Navigate to RemoteOK

            try:
                wait = WebDriverWait(self.driver, 10)  # Waits up to 10 seconds for elements to load
                # Load filters from JSON

                job_title_elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//*[@itemprop='title']")))
                location_elems = wait.until(EC.presence_of_all_elements_located(By.CLASS_NAME, "location"))
                job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@data-url]")))  # Find all <tr> elements with 'data-url'

                self.url_elems = [elem.get_attribute("data-url") for elem in job_elements]
                self.job_title_list = [title.text for title in job_title_elems]
                url_list = []
            except Exception as e:
                print(f"Failed to fetch job information, quitting\n {e}")
                exit()
            for url in self.url_elems:
                display_url = "https://remoteok.com"+url
                url_list.append(display_url)
            company_name_elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h3[@itemprop='name']")))
            company_list = [name.text for name in company_name_elems]
            salary_list = []
            self.location_list = []
            for titl in location_elems:
                if "-" in titl.text:  # Case insensitive search
                    salary_list.append(titl.text.strip())
                else:
                    self.location_list.append(titl.text.strip())

            self.element_to = "⏰ Contractor"
            empty_str = ""
            self.location_list = [item for item in self.location_list if item != self.element_to and item != empty_str]  # Removes all instances of 2
            print(len(self.job_title_list), len(salary_list), len(self.location_list), len(url_list), len(company_list))

            for i in len(self.job_title_list):
                self.jobs.append({"title":self.job_title_list[i], "company":company_list[i], "location":self.location_list[i], "salary":salary_list[i], "url":url_list[i]})
        except Exception as e:
            print(f"Failed to fetch jobs\n {e}")
        self.save_jobs()
    def save_jobs(self):
        try:
            with open("alljobs.json", "w", encoding="utf-8") as file:
                json.dump(self.jobs, file, indent=4)
        except Exception as e:
            print(f"Failed to save jobs\n {e}")

    def extract_salary(self, salary_text):
            salary_text = salary_text.replace("💰", "").replace("$", "").replace("K", "").strip()
            salary_values = re.findall(r"\d+", salary_text)
            return int(salary_values[0]) * 1000 if salary_values else 0

    def filter_jobs_function(self):
        try:
            seen_matches = set()
            self.filtered_jobs = []
            with open("alljobs.json","r",encoding="utf-8") as jobs_file:
                alljobs = json.load(jobs_file)
            try:
                with open("filters.json", "r") as filters_file:
                    filters = json.load(filters_file)
            except FileNotFoundError:
                print("⚠️ Filters file missing! Using default values.")
                filters = {"roles": [], "location": [], "salary": 0}
            except json.JSONDecodeError:
                print("❌ Error parsing filters.json. Check for formatting issues.")
                exit()
            except Exception as e:
                print(f"Failed to load user specified filters, Please try again\n {e}")
            roles = filters["roles"]
            location = filters["location"]
            salary_threshold = filters["salary"]
            try:
                salary_threshold = int(salary_threshold)
            except TypeError:
                print("Salary should contain numbers only, Salary set to default(0)")
                salary_threshold = 0
            except Exception as e:
                print(f"Error occurred, Salary set to default(0)\n {e}")
                salary_threshold = 0
            for job in alljobs:
                title = job["title"]
                job_location = job["location"]
                job_salary = job["salary"]
                company = job["company"]
                url = job["url"]
                salary = self.extract_salary(job_salary)
                cleaned_loc = re.sub(r'[^a-z]','', job_location.lower())
                matched_titles = [keyword for keyword in roles if keyword.lower() in title.lower()]
                matched_location = [locatio for locatio in location if locatio.lower() in cleaned_loc]
                if matched_titles and url not in seen_matches:
                    match_job = {"title": title,
                            "company": company,
                            "salary": job_salary,
                            "location": job_location,
                            "url": url,
                            "matched_filters": {"roles": matched_titles}}
                    if matched_location:
                        match_job["matched_filters"]["location"] = job_location
                        if salary_threshold <= salary:
                            match_job["matched_filters"]["salary"] = job_salary
                            print(title,"->", matched_titles, job_location, job_salary)
                        else:
                            print(title,"->", matched_titles, job_location)
                    else:
                        print(title,"->", matched_titles)
                    seen_matches.add(url)
                    self.filtered_jobs.append(match_job)
                else:
                    print("No matches found!!!")
            total_matched = len(self.filtered_jobs)
            total_filtered = len(self.all_jobs)

            # ✅ Directly write stats inside function
            stats = {"total_filtered": total_filtered, "matched_jobs": total_matched}

            with open("job_stats.json", "w", encoding="utf-8") as file:
                json.dump(stats, file, indent=4)

            print(f"✅ Found {total_matched} matching jobs from {total_filtered} filtered total.")

            with open("matched_jobs.json", "w", encoding="utf-8") as matched_jobs_file:
                json.dump(self.filtered_jobs, matched_jobs_file, indent = 4)
        except Exception as e:
            print(f"An error occurred while filtering Jobs, see details below\n {e}")
            exit()

scraper = remoteok_fetch()
scraper.filter_jobs_function()