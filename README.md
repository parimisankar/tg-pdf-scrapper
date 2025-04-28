## Autorun Setup (Run TG PDF Scrapper on Windows Startup)

### Option 1 — Manual (Task Scheduler)

Follow these steps:
- Open Task Scheduler
- Create Basic Task
- Trigger: At system startup
- Action: Start program -> TG_PDF_Scrapper.exe

(See detailed guide in this repo.)

---

### Option 2 — Automatic (One-click Script)

If you prefer one-click setup:

1. Open PowerShell as Administrator
2. Run:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   cd path\to\TG_PDF_Scrapper\scripts
   .\create_task.ps1