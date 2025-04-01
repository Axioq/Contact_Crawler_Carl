import os
from urllib.parse import urlparse

# This script reads a .txt file containing URLs, cleans them, and returns a list of URLs.
# It ensures that URLs are properly formatted and handles cases where the scheme (http/https) is missing.
def load_urls(file_path):
    """
    Reads a .txt file containing one URL per line, cleans the URLs, and returns a list of URLs.
    If a URL is missing the scheme (http/https), it will be prefixed with 'http://'.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            if not url:
                continue  # Skip empty lines
            
            # Parse URL to check for a scheme; if absent, default to http://
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "http://" + url
            
            urls.append(url)
    return urls

# Main function to execute the script
if __name__ == "__main__":
    # Replace this with your input method or configuration
    config = {
        "txt_file": "websites.txt"  # Update with the actual path if different
    }
    
    try:
        url_list = load_urls(config["txt_file"])
        print("Loaded URLs:")
        for url in url_list:
            print(f" - {url}")
    except Exception as e:
        print(f"Error loading URLs: {e}")