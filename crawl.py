import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright

async def process_website(url, config):
    """
    Processes a single website:
      1. Launches a headless browser.
      2. Navigates to the homepage.
      3. Searches for a contact page using heuristic keywords.
      4. Locates a form on the contact page.
      5. Fills out email, phone, and message fields if found.
      6. Clicks the submit button.
      
    Returns a status string indicating the result.
    """
    try:
        async with async_playwright() as p:
            # Launch a headless Chromium browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # Navigate to the homepage
            await page.goto(url, timeout=60000)
            
            # Heuristic: if the current URL already contains keywords, assume it's the contact page.
            current_url = page.url.lower()
            if any(keyword in current_url for keyword in ["contact", "support", "form"]):
                contact_page_url = page.url
            else:
                # Otherwise, search for a link that might lead to a contact page.
                contact_link = await page.query_selector("a[href*='contact']")
                if contact_link:
                    relative_link = await contact_link.get_attribute("href")
                    # Build full URL if the link is relative
                    contact_page_url = relative_link if relative_link.startswith("http") else urljoin(url, relative_link)
                    await page.goto(contact_page_url, timeout=60000)
                else:
                    print(f"[No contact page] for {url}")
                    await browser.close()
                    return "No contact page found"
            
            # Look for a <form> element on the contact page.
            form = await page.query_selector("form")
            if not form:
                print(f"[No form] found on {contact_page_url}")
                await browser.close()
                return "No form found"
            
            # Heuristically find form fields based on common attributes.
            email_field = await page.query_selector("input[name*='email'], input[id*='email'], input[placeholder*='Email']")
            phone_field = await page.query_selector("input[name*='phone'], input[id*='phone'], input[placeholder*='Phone']")
            message_field = await page.query_selector("textarea[name*='message'], textarea[id*='message'], textarea[placeholder*='Message']")
            
            # Fill out the fields using the values provided in the config.
            if email_field:
                await email_field.fill(config["email"])
            if phone_field:
                await phone_field.fill(config["phone"])
            if message_field:
                await message_field.fill(config["message"])
            
            # Attempt to locate and click a submit button.
            submit_button = await page.query_selector("button[type='submit'], input[type='submit']")
            if submit_button:
                await submit_button.click()
                print(f"[Form submitted] for {url}")
                result = "Form submitted"
            else:
                print(f"[No submit button] found on {url}")
                result = "Submit button not found"
            
            await browser.close()
            return result

    except Exception as e:
        print(f"[Error processing {url}]: {e}")
        return f"Error: {e}"

# For standalone testing:
if __name__ == "__main__":
    # Sample configuration for testing
    sample_config = {
        "email": "axioq28@yahoo.com",
        "phone": "1234567890",
        "message": "Hello, this is a test message!"
    }
    # Replace with a valid URL to test; for example, a site with a contact page.
    test_url = "https://yummygum.com/"
    
    result = asyncio.run(process_website(test_url, sample_config))
    print("Result:", result)