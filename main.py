# main.py
import asyncio
from user_prompt import get_user_inputs
from load_urls import load_urls
from crawl import process_website

async def main():
    # Step 1: Prompt for user inputs.
    config = get_user_inputs()
    
    # Step 2: Load and process URLs from the provided text file.
    try:
        urls = load_urls(config["txt_file"])
        print("\nLoaded URLs:")
        for url in urls:
            print(f" - {url}")
    except Exception as e:
        print(f"Error loading URLs: {e}")
        return
    
    # Step 3: Process each website to fill out the contact form.
    results = []
    for url in urls:
        print(f"\nProcessing website: {url}")
        result = await process_website(url, config)
        results.append((url, result))
    
    # Log results to a file.
    with open("results.log", "w") as log_file:
        for url, status in results:
            log_file.write(f"{url}: {status}\n")
    
    print("\nProcessing complete. Results saved to results.log")

if __name__ == "__main__":
    asyncio.run(main())