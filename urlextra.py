import os
import re
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse, parse_qs

def extract_urls_from_text(text):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.findall(text)

def extract_original_url(safelink_url):
    parsed_url = urlparse(safelink_url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('url', [None])[0]

def process_eml_file(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
        subject = msg.get('subject', 'No Subject')
        payload = msg.get_payload(decode=True)
        if payload:
            text = payload.decode('utf-8', errors='ignore')
            urls = extract_urls_from_text(text)
            extracted_urls = []
            for url in urls:
                if 'safelinks.protection.outlook.com' in url:
                    original_url = extract_original_url(url)
                    if original_url:
                        extracted_urls.append(original_url)
                else:
                    extracted_urls.append(url)
            return subject, extracted_urls
    return None, []

def main():
    eml_files = [f for f in os.listdir() if f.endswith('.eml')]
    
    if not eml_files:
        print("No .eml files found in the current directory.")
        return

    for file in eml_files:
        subject, urls = process_eml_file(file)
        if urls:
            print(f"\nEmail Subject: {subject}")
            for idx, url in enumerate(urls, start=1):
                print(f"{idx}. {url}")

if __name__ == "__main__":
    main()