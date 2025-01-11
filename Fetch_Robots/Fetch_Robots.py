import requests
from urllib.parse import urlparse
import concurrent.futures
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def normalize_url(url):
    """
    Normalize the input URL to ensure it's a valid domain format.
    
    Args:
        url (str): The user-provided URL.
    
    Returns:
        str: A cleaned and normalized domain name.
    
    Raises:
        ValueError: If the input URL is invalid.
    """
    url = url.strip().rstrip('/')
    parsed_url = urlparse(url)
    if not parsed_url.netloc and not parsed_url.path:
        raise ValueError("Invalid input URL. Please enter a valid domain (e.g., example.com).")
    return parsed_url.netloc or parsed_url.path

def create_session_with_retries():
    """
    Creates a requests session with retry logic.
    
    Returns:
        requests.Session: A session object with retry capabilities.
    """
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_robots(url):
    """
    Fetch the robots.txt file from the given URL.
    
    Args:
        url (str): The full URL to the robots.txt file.
    
    Returns:
        str: The content of the robots.txt file or an error message.
    """
    try:
        session = create_session_with_retries()
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return "robots.txt not found."
        return f"Failed to fetch robots.txt. HTTP status: {response.status_code}"
    except requests.RequestException as e:
        return handle_request_error(e)

def fetch_robots_in_parallel(domain):
    """
    Fetch the robots.txt file using both https and http in parallel.
    
    Args:
        domain (str): The domain name (e.g., example.com).
    
    Returns:
        dict: A dictionary with results for 'https' and 'http'.
    """
    schemes = ["https", "http"]
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_scheme = {executor.submit(fetch_robots, f"{scheme}://{domain}/robots.txt"): scheme for scheme in schemes}
        for future in concurrent.futures.as_completed(future_to_scheme):
            scheme = future_to_scheme[future]
            try:
                results[scheme] = future.result()
            except Exception as exc:
                results[scheme] = f"Failed with error: {exc}"
    return results

def handle_request_error(exception):
    """
    Handle errors during the request.
    
    Args:
        exception (Exception): The exception raised during the request.
    
    Returns:
        str: A user-friendly error message.
    """
    if isinstance(exception, requests.Timeout):
        return "Request timed out. Please check your network and try again."
    elif isinstance(exception, requests.ConnectionError):
        return "Failed to connect to the server. Please check the URL."
    return f"An unexpected error occurred: {exception}"

def parse_robots_txt(content):
    """
    Parse the content of robots.txt for key directives like Sitemap or Disallow.
    
    Args:
        content (str): The content of the robots.txt file.
    
    Returns:
        dict: A dictionary with parsed directives.
    """
    directives = {}
    for line in content.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            directives.setdefault(key, []).append(value)
    return directives

if __name__ == "__main__":
    domain = input("Enter the website domain (e.g., example.com): ")
    try:
        domain = normalize_url(domain)
        results = fetch_robots_in_parallel(domain)
        for scheme, result in results.items():
            print(f"\n--- Results for {scheme.upper()} ---")
            if "not found" in result.lower() or "error" in result.lower():
                print(result)
            else:
                print("robots.txt content:\n", result)
                # Optionally parse and display directives
                directives = parse_robots_txt(result)
                print("\nParsed Directives:")
                for key, values in directives.items():
                    print(f"{key}: {', '.join(values)}")
    except ValueError as e:
        print(e)
