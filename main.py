import os
import asyncio
import datetime
import json
from pyrogram import Client
from pyrogram.errors import FloodWait

# Create download folder
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Save config
def save_config(config_data):
    with open('config.json', 'w') as f:
        json.dump(config_data, f)

# Load config
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    return None

# Save downloaded file list
def save_downloaded_list(file_list):
    with open('downloaded_pdfs.txt', 'w', encoding='utf-8') as f:
        for item in file_list:
            f.write(f"{item}\n")

# Load downloaded file list
def load_downloaded_list():
    if os.path.exists('downloaded_pdfs.txt'):
        with open('downloaded_pdfs.txt', 'r') as f:
            return f.read().splitlines()
    return []

async def main():
    config = load_config()

    if not config:
        print("First time setup...")
        api_id = int(input("Enter your Telegram API ID: "))
        api_hash = input("Enter your Telegram API HASH: ")
        phone = input("Enter your phone number (with country code): ")
        channels_input = input("Enter Telegram channel usernames (comma separated, e.g., researchreportss, btsreports): ")
        download_folder = input("Enter full download folder path (e.g., C:\\Users\\JaiParimi\\TG_PDF_Scrapper\\Downloads): ")

        config = {
            "api_id": api_id,
            "api_hash": api_hash,
            "phone": phone,
            "channels": [ch.strip() for ch in channels_input.split(',')],
            "download_folder": download_folder
        }
        save_config(config)

    app = Client("tg_pdf_scrapper_session", api_id=config['api_id'], api_hash=config['api_hash'], phone_number=config['phone'])
    downloaded_files = load_downloaded_list()

    create_folder(config['download_folder'])

    async with app:
        while True:
            try:
                print(f"\nRunning scheduled sync at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                new_downloads = 0
                total_found = 0

                for channel in config['channels']:
                    try:
                        async for message in app.get_chat_history(channel, limit=100):
                            if (datetime.datetime.now(datetime.timezone.utc) - message.date.replace(tzinfo=datetime.timezone.utc)).days <= 7:
                                if message.document and message.document.mime_type == "application/pdf":
                                    file_name = message.document.file_name
                                    if file_name not in downloaded_files:
                                        total_found += 1
                                        await message.download(file_name=os.path.join(config['download_folder'], file_name))
                                        downloaded_files.append(file_name)
                                        new_downloads += 1
                                    else:
                                        total_found += 1
                            else:
                                break
                    except FloodWait as e:
                        print(f"Sleeping for {e.value} seconds due to Telegram FloodWait...")
                        await asyncio.sleep(e.value)

                save_downloaded_list(downloaded_files)

                print("\n===================================")
                print(f"TG PDF Scrapper - Sync Complete")
                print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
                print(f"Channels Checked: {len(config['channels'])}")
                print(f"Total PDFs Found: {total_found}")
                print(f"New PDFs Downloaded: {new_downloads}")
                print(f"Already Existing PDFs Skipped: {total_found - new_downloads}")
                print("Next scan will run in 24 hours...")
                print("===================================\n")

                await asyncio.sleep(86400)  # 24 hours sleep

            except OSError as e:
                print(f"\n⚡ Socket error encountered: {e}")
                print("🔄 Attempting silent reconnection after 120 seconds...")
                await asyncio.sleep(120)  # Sleep for 2 minutes
                continue  # Retry the loop

if __name__ == "__main__":
    asyncio.run(main())