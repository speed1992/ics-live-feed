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

To add this live feed to your personal calendar, copy the raw URL below:

> **Feed URL:** > `https://raw.githubusercontent.com/speed1992/ics-live-feed/refs/heads/main/delhi_screenings.ics`

### 💻 Initial Desktop Setup (Google Calendar)
*Note: Do this initial setup on a computer browser for the best results.*

1. Open **[Google Calendar](https://calendar.google.com/)**.
2. On the left sidebar, next to **Other calendars**, click the `+` (plus) icon.
3. Select **From URL**.
4. Paste the Feed URL and click **Add calendar**. 
*(Optional: Go to the calendar settings and rename it to "CatchAFilm Delhi" for a cleaner look).*

---

## 📱 Mobile Sync & Troubleshooting Guide

Web-subscribed calendars often do not sync to mobile apps automatically. Find your device below to force the sync.

### 🤖 Android Devices
**The Issue:** Google Calendar does not push web subscriptions to the Android app by default.  
**The Fix:**
1. Open the **Google Calendar app** on your phone.
2. Tap the **Menu ☰** (top-left) and scroll to **Settings**.
3. Tap your **Google Account** name, and find the new calendar (Tap *"Show more"* if it's hidden).
4. Tap the calendar and toggle **Sync** to **ON**.
5. Return to the main calendar view, tap the Menu, and hit **Refresh**.

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

This repository is designed to be entirely self-sufficient. A GitHub Action runs daily at midnight UTC, executes the Playwright scraper, and commits any new movie screenings back to the `.ics` file. 

<details>
<summary><strong>📦 requirements.txt</strong></summary>

```text
playwright>=1.48.0
ics==0.7.2
