# 🍿 CatchAFilm: Delhi Film Screenings ICS Feed

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Async-green)](https://playwright.dev/python/)
[![Automated via GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-orange)](https://github.com/features/actions)

An automated web scraper and calendar generator that extracts local film screening schedules in Delhi and converts them into a live, subscribable iCalendar (`.ics`) feed. 

This project uses an asynchronous headless browser with anti-bot masking to bypass dynamic loading, generating a real-time calendar feed that plugs directly into Google Calendar, Apple Calendar, or Outlook.

---

## 📅 Subscribing to the Live Feed

To add this live feed to your personal calendar, copy the raw URL below:

```text
[https://raw.githubusercontent.com/speed1992/ics-live-feed/refs/heads/main/delhi_screenings.ics](https://raw.githubusercontent.com/speed1992/ics-live-feed/refs/heads/main/delhi_screenings.ics)

### 💻 Step 1: Initial Desktop Setup (Google Calendar)
*It is highly recommended to do the initial setup on a computer browser.*

1. Open [Google Calendar](https://calendar.google.com/).
2. On the left sidebar, next to **Other calendars**, click the `+` (plus) icon.
3. Select **From URL**.
4. Paste the raw URL copied above and click **Add calendar**. 
*(Optional: Go to the calendar settings and rename it to "CatchAFilm Delhi" for better readability).*

### 🤖 Step 2: Android Setup & Troubleshooting
**The Expected Issue:** Google Calendar does not automatically push newly subscribed web feeds to the Android app. You must force the sync.

**The Solution:**
1. Open the **Google Calendar app** on your Android phone.
2. Tap the **Menu** (three horizontal lines) in the top-left.
3. Scroll to the very bottom and tap **Settings**.
4. Tap on your **Google Account**, then find the newly added calendar. *(If you don't see it, tap "Show more" under your account).*
5. Tap the calendar, and toggle **Sync** to the **ON** position.
6. Return to your main calendar view, tap the Menu again, and hit **Refresh** (or swipe down from the top). 

### 🍎 Step 3: Apple iOS Setup & Troubleshooting
iOS users have two ways to view the calendar, each with a specific fix for delayed syncing.

**Method A: Subscribe directly via iOS Settings (Recommended)**
1. On your iPhone, open **Settings** > **Calendar** > **Accounts**.
2. Tap **Add Account** > **Other**.
3. Tap **Add Subscribed Calendar**.
4. Paste the raw URL and tap **Next**, then **Save**.
* **Fixing Sync Delays:** iOS caches calendars aggressively. To ensure it updates live, go back to **Settings** > **Calendar** > **Accounts** > **Fetch New Data**. Ensure your subscribed calendar is set to **Fetch** (not Manual), and set the global fetch schedule at the bottom to **Every 15 Minutes** or **Hourly**.

**Method B: Syncing from your Google Account to Apple Calendar**
**The Expected Issue:** If you added the URL to Google Calendar on your desktop, Apple Calendar often hides "Other/Subscribed" Google calendars by default.
**The Solution:**
1. Open Safari on your iPhone and go to this exact hidden Google settings page: `https://calendar.google.com/calendar/syncselect`
2. Check the box next to your new Delhi Film Screenings calendar.
3. Click **Save** in the bottom right corner.
4. Open the Apple **Calendar** app, tap **Calendars** at the bottom, and pull down to refresh.
