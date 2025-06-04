# **JobSentry**
🚀 **Automated job scraper for RemoteOK** that fetches job listings, filters them based on user preferences, and sends notifications via email.

## **📌 Features**
✅ **Automated job fetching** using Selenium  
✅ **Filter jobs based on roles, location, and salary** via CLI or JSON  
✅ **Saves job listings in structured JSON files**  
✅ **Runs daily via scheduling**  

---

## **🛠 Installation & Setup**
### **1️⃣ Prerequisites**
- Python **>= 3.8**
- `pip` (Python package manager)
- Google Chrome & ChromeDriver (OR Edge & EdgeDriver)
- Dependencies in `requirements.txt`

### **2️⃣ Install Dependencies**
Run the following:
```bash
pip install -r requirements.txt
```

### **3️⃣ Verify WebDriver Installation**
Ensure you have the correct **ChromeDriver** version installed:
```bash
chrome://settings/help  # Check Chrome version
```
If the version differs, download the matching **ChromeDriver** from:
➡ [https://sites.google.com/chromium.org/driver](https://sites.google.com/chromium.org/driver)

---

## **⚙️ Usage**
### **Run the Scraper**
You can run the script with default filters:
```bash
python main.py
```
OR specify custom filters via CLI:
```bash
python main.py --roles Developer Designer --location Remote --salary 80000
```

### **Filter Explanation**
🔹 **Roles**: Job titles to filter (e.g., `Developer`, `Designer`)  
🔹 **Location**: Preferred job locations (e.g., `Remote`, `USA`)  
🔹 **Salary**: Minimum salary threshold (e.g., `80000` for $80K)

---

## **💾 Output Files**
The scraper generates structured JSON files:
| File Name          | Description |
|--------------------|-------------|
| `alljobs.json`    | Contains **all fetched jobs** |
| `matched_jobs.json` | Contains **filtered jobs** |
| `filters.json`    | Stores **latest user-defined filters** |

---

## **🔄 Automating Daily Execution**
To schedule the script to run **every day**, use one of the following:

### **Linux/macOS (Cron Job)**
1️⃣ Open terminal and type:
```bash
crontab -e
```
2️⃣ Add this line to run the script at **8 AM daily**:
```bash
0 8 * * * /usr/bin/python3 /path/to/main.py
```

### **Windows (Task Scheduler)**
1️⃣ Open **Task Scheduler** → **Create Basic Task**  
2️⃣ Set trigger to **Daily** at **8 AM**  
3️⃣ Set action to **Run a program** → Select `python.exe` and `main.py`

### **Python-based Scheduling**
Alternatively, use Python’s **`schedule`** module:
```python
import schedule
import time

def run_scraper():
    scraper = remoteok_fetch()
    scraper.fetch_jobs_function()
    scraper.filter_jobs_function()
    send_email()  # Implement your email function

schedule.every().day.at("08:00").do(run_scraper)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

---

## **🛠 Troubleshooting**
### **WebDriver Issues**
❌ **Error: WebDriver not found**  
✔ **Solution:** Ensure ChromeDriver **matches Chrome version**  
✔ **Fix:** Download the correct driver from [Google ChromeDriver](https://sites.google.com/chromium.org/driver)

### **Filtering Errors**
❌ **Error: No jobs matching filters**  
✔ **Fix:** Double-check filters in `filters.json`  
✔ **Run script with CLI arguments to override**:
```bash
python main.py --roles Developer --location Remote
```

---

## **👨‍💻 Contributors**
- **Mitarumi** ✨ _Main developer_
