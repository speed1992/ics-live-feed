import asyncio
import urllib.parse
import re
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright
from ics import Calendar, Event

URL = "https://fillum.in/film-screenings-in-delhi"
BASE_URL = "https://fillum.in"

async def scrape_and_generate_calendar():
    async with async_playwright() as p:
        # 1. Mask automation flags for maximum stealth
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
        
        try:
            await page.goto(URL, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"Failed to load page: {e}")
            await browser.close()
            return
            
        print(f"Loaded Page Title: {await page.title()}")

        # 3. Explicitly wait for the first screening box to appear
        try:
            await page.wait_for_selector(".screeninginfo", timeout=15000)
            print("Successfully found screening data!")
        except Exception as e:
            print("ERROR: Could not find any events. Site might be blocking or DOM changed.")
            await browser.close()
            return

        print("Scrolling to load all events...")
        same_count = 0

        # 4. Infinite Scroll with jittered waits (Anti-Bot)
        while True:
            old_height = await page.evaluate("document.documentElement.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            await page.wait_for_timeout(random.randint(1500, 2500))
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
            # Wrap the entire card parser in a try/except so one badly malformed card doesn't crash the loop
            try:
                # Use .first to prevent strict-mode errors if the DOM accidentally duplicates classes
                title_loc = card.locator(".scfilmname > a")
                title = await title_loc.first.inner_text() if await title_loc.count() > 0 else "Unknown Title"

                location_loc = card.locator(".sclocation")
                location = await location_loc.first.inner_text() if await location_loc.count() > 0 else "Unknown Location"

                host_loc = card.locator(".schost")
                host = await host_loc.first.inner_text() if await host_loc.count() > 0 else ""
                host = " ".join(host.split())

                desc_loc = card.locator(".scdescription")
                description = await desc_loc.first.inner_text() if await desc_loc.count() > 0 else ""

                details_loc = card.locator(".screeningdetails")
                raw_details = await details_loc.first.inner_text() if await details_loc.count() > 0 else ""

                # --- DEFENSIVE URL EXTRACTION ---
                absolute_url = None
                fallback_url = f"{BASE_URL}/film-screenings-in-delhi"

                def is_valid_path(path):
                    if not path:
                        return False
                    path = str(path).strip()
                    invalid_exacts = {"", "#", "javascript:void(0)", "javascript:;"}
                    if path in invalid_exacts or path.startswith("javascript:"):
                        return False
                    return True

                try:
                    # LAYER 1: Ticket button
                    ticket_loc = card.locator(".ticketbtn")
                    if await ticket_loc.count() > 0:
                        candidate1 = await ticket_loc.first.get_attribute("href")
                        if is_valid_path(candidate1):
                            absolute_url = urllib.parse.urljoin(BASE_URL, candidate1)

                    # LAYER 2: Title link
                    if not absolute_url:
                        if await title_loc.count() > 0:
                            candidate2 = await title_loc.first.get_attribute("href")
                            if is_valid_path(candidate2):
                                absolute_url = urllib.parse.urljoin(BASE_URL, candidate2)

                    # LAYER 3: Structural ID Fallback
                    if not absolute_url:
                        card_id = await card.get_attribute("id") 
                        if card_id and str(card_id).startswith("Screening"):
                            event_id = str(card_id).replace("Screening", "").strip()
                            if event_id.isdigit():
                                absolute_url = f"{BASE_URL}/screening/{event_id}"

                except Exception as e:
                    print(f"Warning: URL extraction issue for '{title}'. Error: {e}")

                # LAYER 4: Ultimate Safety Net
                if not absolute_url:
                    absolute_url = fallback_url
                # --------------------------------

                # Date parsing
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
                        
                        url_text = f"\n\nMore info / Tickets: {absolute_url}"
                        event.description = f"Host: {host}\n\n{description.strip()}{url_text}"
                        
                        cal.events.add(event)
                        success_count += 1
                    except ValueError as e:
                        print(f"Date parsing error for '{title}': {e}")
                else:
                    print(f"Could not find valid date string for '{title}'")
            
            except Exception as e:
                print(f"Warning: Unexpected error processing card '{title}'. Skipping. Error: {e}")

        await browser.close()

        # Write out the final ICS file
        with open('delhi_screenings.ics', 'w', encoding='utf-8') as f:
            f.write(cal.serialize())
            
        print(f"Done! Generated delhi_screenings.ics with {success_count} events.")

if __name__ == "__main__":
    asyncio.run(scrape_and_generate_calendar())
