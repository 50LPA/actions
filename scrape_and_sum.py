import asyncio
from playwright.async_api import async_playwright

async def scrape_and_sum_tables():
    """
    Visits a series of web pages, scrapes all numbers from tables,
    and calculates their total sum.
    """
    base_url = "http://www.example.com/data_report/seed/{}" # Placeholder URL, replace with actual
    seeds = range(25, 35) # Seeds from 25 to 34

    total_sum = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for seed in seeds:
            url = base_url.format(seed)
            print(f"Navigating to: {url}")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000) # Increased timeout
                print(f"Successfully navigated to {url}")

                # Find all table cells (td and th) that contain numbers
                # This XPath selects text nodes directly within td/th elements,
                # or within immediate children like <span>, and filters for digits.
                # It's robust for various table structures.
                number_elements = await page.locator(
                    "//table//td[normalize-space() != ''] | //table//th[normalize-space() != '']"
                ).all()

                page_numbers_sum = 0
                for element in number_elements:
                    text_content = await element.text_content()
                    if text_content:
                        # Use regex to find all numbers (integers or floats) in the text
                        # This handles cases where text might be "Value: 123"
                        numbers_in_text = re.findall(r'-?\d+\.?\d*', text_content)
                        for num_str in numbers_in_text:
                            try:
                                # Try converting to float first for decimals, then int
                                if '.' in num_str:
                                    num = float(num_str)
                                else:
                                    num = int(num_str)
                                page_numbers_sum += num
                            except ValueError:
                                # Not a valid number, skip
                                pass
                print(f"Sum for {url}: {page_numbers_sum}")
                total_sum += page_numbers_sum

            except Exception as e:
                print(f"Error processing {url}: {e}")
                # Continue to next page even if one fails

        await browser.close()
    print(f"\nTotal sum of all numbers across all tables: {total_sum}")

if __name__ == "__main__":
    import re # Import re here as well for direct execution
    asyncio.run(scrape_and_sum_tables())

