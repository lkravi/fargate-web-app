import requests
from playwright.sync_api import sync_playwright
import time

def wait_for_service(url, timeout=30):
    """Wait for the service at the specified URL to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(1)
    return False

def test_backend():
    assert wait_for_service("http://backend:5001/api/books"), "Backend service is not available"
    response = requests.get("http://backend:5001/api/books")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_frontend():
    print("Waiting for the frontend service to be available...")
    assert wait_for_service("http://frontend:8080"), "Frontend service is not available"
    
    print("Launching browser and accessing the frontend...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()
        
        print("Navigating to the frontend URL...")
        page.goto("http://frontend:8080")
        print("Page title:", page.title())
        assert "frontend" in page.title().lower()
        
        # Wait for the specific content to be loaded
        print("Waiting for the book list items to load...")
        page.wait_for_selector('ul > li')
        
        # Check if the books are listed in the frontend
        print("Fetching book list items from the page...")
        book_list_items = page.query_selector_all('ul > li')
        book_titles = [item.text_content() for item in book_list_items]
        print("Book titles found:", book_titles)
        
        assert "Head First Java by Robert C. Martin" in book_titles

if __name__ == "__main__":
    test_frontend()
