import asyncio
import urllib.parse
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright
from ics import Calendar, Event

URL = "https://fillum.in/film-screenings-in-delhi"
BASE_URL = "https://fillum.in"

async def scrape_and_generate_calendar():
    async with async_playwright() as p:
        # 1. Mask the automation flags to bypass basic bot detection
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        
        # 2. Forge a realistic User-Agent and viewport
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        print(f"Navigating to {URL}...")
        # 3. Wait until network activity settles
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        
        # Print the page title for debugging in GitHub logs
        print(f"Loaded Page Title: {await page.title()}")

        # 4. Explicitly wait for the first screening box to appear
        try:
            await page.wait_for_selector(".screeninginfo", timeout=15000)
            print("Successfully found screening data!")
        except Exception as e:
            print("ERROR: Could not find any events. The site might be blocking GitHub Actions.")
            html = await page.content()
            print(f"Page HTML Snippet: {html[:500]}")
            await browser.close()
            return

        print("Scrolling to load all events...")
        same_count = 0

        # --- Infinite Scroll ---
        while True:
            old_height = await page.evaluate("document.documentElement.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            await page.wait_for_timeout(2000)
            new_height = await page.evaluate("document.documentElement.scrollHeight")

            if new_height == old_height:
                same_count += 1
            else:
                same_count = 0

            if same_count >= 3:
                break
        
        cal = Calendar()
        event_cards = await page.locator(".screeninginfo").all()
        success_count = 0

        print(f"Found {len(event_cards)} event cards. Parsing...")

        for card in event_cards:
            title_loc = card.locator(".scfilmname > a")
            title = await title_loc.inner_text() if await title_loc.count() > 0 else "Unknown Title"

            location_loc = card.locator(".sclocation")
            location = await location_loc.inner_text() if await location_loc.count() > 0 else "Unknown Location"

            host_loc = card.locator(".schost")
            host = await host_loc.inner_text() if await host_loc.count() > 0 else ""
            host = " ".join(host.split())

            desc_loc = card.locator(".scdescription")
            description = await desc_loc.inner_text() if await desc_loc.count() > 0 else ""

            url_loc = card.locator(".ticketbtn")
            raw_url = await url_loc.get_attribute("href") if await url_loc.count() > 0 else None
            if not raw_url:
                raw_url = await title_loc.get_attribute("href") if await title_loc.count() > 0 else None
            absolute_url = urllib.parse.urljoin(BASE_URL, raw_url) if raw_url else None

            details_loc = card.locator(".screeningdetails")
            raw_details = await details_loc.inner_text() if await details_loc.count() > 0 else ""

            date_match = re.search(r'(\d{1,2} [A-Za-z]{3}, \d{4} · \d{1,2}:\d{2} [APM]{2})', raw_details)
            
            if date_match:
                date_str = date_match.group(1)
                try:
                    start_time = datetime.strptime(date_str, "%d %b, %Y · %I:%M %p")
                    start_time = start_time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
                    
                    event = Event()
                    event.name = title.strip()
                    event.begin = start_time
                    event.duration = timedelta(hours=2) 
                    event.location = location.strip()
                    event.url = absolute_url
                    url_text = f"\n\nMore info / Tickets: {absolute_url}" if absolute_url else ""
                    event.description = f"Host: {host}\n\n{description.strip()}{url_text}"
                    # event.description = f"Host: {host}\n\n{description.strip()}"
                    
                    cal.events.add(event)
                    success_count += 1
                except ValueError as e:
                    print(f"Date parsing error for {title}: {e}")

        await browser.close()

        # Write out the final ICS file
        with open('delhi_screenings.ics', 'w', encoding='utf-8') as f:
            f.writelines(cal.serialize_iter())
            
        print(f"Done! Generated delhi_screenings.ics with {success_count} events.")

# Use asyncio.run() since this runs natively in GitHub Actions, not inside a Colab notebook
asyncio.run(scrape_and_generate_calendar())