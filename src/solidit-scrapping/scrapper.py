import requests
from flask import Flask, jsonify
import os
import json
import pdfkit
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Directory to save PDF reports
REPORTS_DIR = './audits-reports'
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# Credentials for Solodit
EMAIL = "testingforever121@gmail.com"
PASSWORD = "ethglobalbrussels"

# Session object to manage cookies and headers across requests
session = requests.Session()

def login():
    """ Login to the site by first fetching CSRF token from HTML, then authenticate. """
    pre_login_url = "https://solodit.xyz/auth?next=/login"
    response = session.get(pre_login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value') if soup.find('input', {'name': 'csrfmiddlewaretoken'}) else None

    if csrf_token:
        print("CSRF Token:", csrf_token)
        login_url = "https://solodit.xyz/auth"
        credentials = {'email': EMAIL, 'password': PASSWORD, 'csrfmiddlewaretoken': csrf_token}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        login_response = session.post(login_url, data=credentials, headers=headers)
        print("Login Response Status:", login_response.status_code)
    else:
        print("CSRF token not found.")

def fetch_tree_and_generate_pdfs():
    """Fetch data from /tree endpoint and generate PDFs from reference links."""
    tree_url = "https://solodit.xyz/checklist"
    tree_response = session.get(tree_url)
    print("Tree Response Status:", tree_response.status_code)

    if tree_response.ok:
        try:
            tree_data = tree_response.json()
            extract_and_download_pdfs(tree_data)
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)

def extract_and_download_pdfs(data):
    """Recursively extract URLs from reference lists and generate PDFs."""
    if 'childs' in data:
        for child in data['childs']:
            extract_and_download_pdfs(child)
    elif 'referenceList' in data and data.get('isLeaf', False):
        for url in data['referenceList']:
            filename = url.split('/')[-1] + ".pdf"
            save_pdf(url, filename)

def save_pdf(url, filename):
    """Save the webpage as a PDF file."""
    response = session.get(url)
    if response.ok:
        pdf_path = os.path.join(REPORTS_DIR, filename)
        pdfkit.from_string(response.text, pdf_path)
        print(f"Saved PDF for {url} as {filename}")
    else:
        print(f"Failed to fetch {url}, status code {response.status_code}")

scheduler = BackgroundScheduler()
scheduler.add_job(login, 'interval', hours=24)
scheduler.add_job(fetch_tree_and_generate_pdfs, 'interval', hours=24)
scheduler.start()

@app.route('/reports')
def list_reports():
    """ List all reports saved in the directory as JSON. """
    reports = os.listdir(REPORTS_DIR)
    return jsonify(reports)

if __name__ == '__main__':
    login()  # Perform initial login
    fetch_tree_and_generate_pdfs()  # Fetch and process data after login
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Ensure cert files are in the correct directory
