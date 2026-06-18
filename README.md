<p align="center">
  <h1 align="center">🍿 CatchAFilm</h1>
  <p align="center"><strong>Live Delhi Film Screenings ICS Feed</strong></p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Playwright-Async-green" alt="Playwright">
  <img src="https://img.shields.io/badge/GitHub%20Actions-Automated-orange" alt="GitHub Actions">
</p>

---

An automated web scraper and calendar generator that extracts local film screening schedules in Delhi and converts them into a live, subscribable iCalendar (`.ics`) feed. 

This project uses an asynchronous headless browser with anti-bot masking to bypass dynamic loading, generating a real-time calendar feed that plugs directly into **Google Calendar**, **Apple Calendar**, or **Outlook**.

---

## 📅 Quick Subscribe

To add this live feed to your personal calendar, copy the URL below:

> **Feed URL:** > `https://speed1992.github.io/ics-live-feed/`

## 📱 Mobile Sync & Troubleshooting Guide

Web-subscribed calendars often do not sync to mobile apps automatically. Find your device below to force the sync.

### 🤖 Android Devices & Google Calendar App
**The Core Issue:** When you subscribe to a calendar via URL on your desktop, Google does not automatically push that new subscription to your mobile app to save data. You have to manually activate it.

**Step-by-Step Fix:**
1. Open the **Google Calendar app** on your Android phone.
2. Tap the **Menu ☰** (the three horizontal lines in the top-left corner).
3. Scroll all the way to the bottom and tap **Settings** (⚙️).
4. Tap on the **Google Account** where you added the calendar subscription.
5. **CRITICAL STEP:** Look for the new calendar. If you don't see it immediately, you *must* tap **"Show more"** under that account section. It is almost always hidden here by default.
   * *Note: The calendar might be named with the GitHub URL instead of "CatchAFilm" initially. Look for that specific link!*
6. Tap on the calendar name.
7. Toggle the **Sync** switch at the very top to the **ON** (blue) position.
8. Return to your main calendar view. Tap the Menu again and hit **Refresh** (or simply pull down firmly from the top of the screen). Give it a few seconds to pull the live data.

**Still not seeing it? (Advanced Troubleshooting):**
* **Clear App Cache:** Go to your Android phone's main **Settings** > **Apps** > **Calendar** > **Storage** > **Clear Cache**. Re-open the app and pull down to refresh.
* **Check Global OS Sync:** Go to your phone's main **Settings** > **Passwords & accounts** (or **Accounts**) > tap your **Google** account > **Account sync** > ensure the toggle for "Calendar" is switched on.

### 🍎 Apple iOS Devices
iOS caches calendars aggressively. Choose one of the two methods below to ensure your feed stays live.

**Method A: Direct iOS Subscription (Recommended)**
1. Open **Settings** > **Calendar** > **Accounts**.
2. Tap **Add Account** > **Other** > **Add Subscribed Calendar**.
3. Paste the Feed URL and hit **Save**.
4. *To fix sync delays:* Go to **Fetch New Data** in the Accounts menu, set the calendar to **Fetch**, and set the global schedule to **Hourly**.

**Method B: Syncing via Google Account**
1. Open Safari on your iPhone and log into this hidden Google sync page:  
   [`https://calendar.google.com/calendar/syncselect`](https://calendar.google.com/calendar/syncselect)
2. Check the box next to your new CatchAFilm calendar and click **Save**.
3. Open the Apple **Calendar** app, tap **Calendars** at the bottom, and pull down to refresh.

---

## 🛠️ Project Architecture

This repository is designed to be entirely self-sufficient. A GitHub Action runs daily at midnight UTC, executes the Playwright scraper, and commits any new movie screenings back to the repository, updating the GitHub Pages site.

<details>
<summary><strong>📦 requirements.txt</strong></summary>

```text
playwright>=1.48.0
ics==0.7.2
pytz>=2024.1
