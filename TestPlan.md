# TG PDF Scrapper Test Plan

## Objective
Verify that TG PDF Scrapper runs correctly, downloads PDFs, handles errors, and maintains scheduled operations.

---

## Test Cases

| Step | Expected Result |
|:---|:---|
| Launch app | App starts without errors |
| First-time login | User enters API ID, Hash, Phone |
| Channel input | Channels accepted and stored |
| PDF sync | PDFs downloaded from channels |
| Duplicate PDFs | Already existing PDFs skipped |
| Unicode filenames | Files saved properly |
| Socket errors | Bot silently reconnects after 2 minutes |
| FloodWait errors | Bot respects Telegram limits |
| 24-hour sleep | Bot sleeps and wakes up correctly |

---

## Bonus Tests
- Test interrupted internet connection.
- Test invalid channel usernames.
- Test non-PDF attachments (should ignore).

---

✅ End of TestPlan