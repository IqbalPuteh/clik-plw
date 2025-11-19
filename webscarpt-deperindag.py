import time
import csv
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Global variables
browser = None
page = None
all_data = []

def initialize_browser(headless=True):
    """Initialize the browser with Playwright"""
    global browser, page
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    
    # Set viewport size
    page.set_viewport_size({"width": 1920, "height": 1080})

def set_date_filter():
    """Set the date filter to 01/01/2000"""
    global page
    
    try:
        # Wait for the date input to be present
        page.wait_for_selector("#tanggal_mulai", timeout=60000)
        
        # Set the date value to 01/01/2000
        page.fill("#tanggal_mulai", "1980-01-01")
        
        print("Date filter set to 01/01/1980")
        
        # Wait a moment for any JavaScript to process the change
        time.sleep(2)
        
    except Exception as e:
        print(f"Error setting date filter: {e}")

def extract_table_data():
    """Extract data from the table with class 'table table-bordered table-striped'"""
    global page
    
    try:
        # Wait for table to be present
        page.wait_for_selector("table.table.table-bordered.table-striped", timeout=60000)
        
        # Get table HTML
        table_html = page.inner_html("table.table.table-bordered.table-striped")
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Extract headers (if they exist)
        headers = []
        header_row = soup.find('thead')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        else:
            # If no thead, try to get headers from first row
            first_row = soup.find('tr')
            if first_row:
                headers = [td.get_text(strip=True) for td in first_row.find_all(['th', 'td'])]
        
        # Extract all rows
        rows = []
        tbody = soup.find('tbody')
        if tbody:
            table_rows = tbody.find_all('tr')
        else:
            table_rows = soup.find_all('tr')[1:]  # Skip header row if no tbody
        
        for row in table_rows:
            cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
            if cells:  # Only add non-empty rows
                rows.append(cells)
        
        return headers, rows
        
    except Exception as e:
        print(f"Error extracting table data: {e}")
        return [], []

def find_next_button():
    """Find the 'Selanjutnya' (Next) button"""
    global page
    
    selectors = [
        "button:has-text('Selanjutnya')",
        "a:has-text('Selanjutnya')",
        "input[value='Selanjutnya']",
        "button.next",
        "a.next"
    ]
    
    for selector in selectors:
        try:
            button = page.query_selector(selector)
            if button and button.is_visible() and button.is_enabled():
                return button
        except Exception:
            continue
    
    return None

def save_data(headers, output_file):
    """Save scraped data to CSV file"""
    global all_data
    
    if not all_data:
        print("No data to save")
        return
    
    try:
        # Create DataFrame
        if headers:
            df = pd.DataFrame(all_data, columns=headers)
        else:
            df = pd.DataFrame(all_data)
        
        # Save to CSV
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Data saved to {output_file}")
        print(f"Total rows scraped: {len(all_data)}")
        
        # Also save as Excel for better formatting
        excel_file = output_file.replace('.csv', '.xlsx')
        df.to_excel(excel_file, index=False)
        print(f"Data also saved to {excel_file}")
        
    except Exception as e:
        print(f"Error saving data: {e}")

def scrape_all_pages(url, output_file="scraped_data.csv", headless=True):
    """Main scraping function that handles pagination"""
    global browser, page, all_data
    
    try:
        # Initialize browser
        initialize_browser(headless)
        
        print(f"Opening URL: {url}")
        page.goto(url)
        page.wait_for_load_state('networkidle')
        
        # Set the date filter before scraping
        set_date_filter()
        
        page_count = 1
        all_headers = []
        
        while True:
            print(f"Scraping page {page_count}...")
            
            # Extract data from current page
            headers, rows = extract_table_data()
            
            if not rows:
                print("No data found on this page")
                break
            
            # Store headers from first page
            if page_count == 1:
                all_headers = headers
            
            # Add page data to our collection
            for row in rows:
                all_data.append(row)
            
            print(f"Extracted {len(rows)} rows from page {page_count}")
            
            # Look for the "Selanjutnya" button
            next_button = find_next_button()
            
            if next_button:
                print("Found 'Selanjutnya' button, clicking...")
                try:
                    # Scroll to button and click
                    next_button.scroll_into_view_if_needed()
                    time.sleep(1)
                    next_button.click()
                    page.wait_for_load_state('networkidle')
                    time.sleep(2)  # Additional wait for page to load
                    page_count += 1
                except Exception as e:
                    print(f"Error clicking next button: {e}")
                    break
            else:
                print("No 'Selanjutnya' button found - scraping complete!")
                break
        
        # Save all collected data
        save_data(all_headers, output_file)
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        if browser:
            browser.close()

def main():
    # Replace with your target URL
    url = "https://ditjenpdn.kemendag.go.id/setiap-saat/izin-terbit/siupl"
    #url ="https://ditjenpdn.kemendag.go.id/setiap-saat/izin-terbit/stpagen"
    # Start scraping
    scrape_all_pages(url, "table_data.csv", headless=True)

if __name__ == "__main__":
    main()