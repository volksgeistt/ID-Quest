import requests
import asyncio
import aiohttp
import sys
import itertools

def fetch_platforms():
    url = "https://snatcher.netlify.app/platforms.json"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SnatcherBot/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise ValueError("Expected JSON response")
        return response.json()
    except Exception as e:
        print(f"Error fetching platform data: {e}")
    return {}

async def check_username(session, platform, data, username):
    url = data["url"].format(username)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SnatcherBot/1.0)"}
    try:
        async with session.get(url, timeout=10, headers=headers) as response:
            text = await response.text()
            status_code = response.status

            if data["expected_text"].lower() in text.lower():
                return (platform, "Available", "✅")
            elif status_code == 404:
                return (platform, "Available", "✅")
            elif status_code == 200:
                return (platform, "Taken or Unknown", "❌")
            elif status_code == 403:
                return (platform, "Forbidden (403)", "⚠️")
            else:
                return (platform, f"Unknown ({status_code})", "⚠️")

    except asyncio.TimeoutError:
        return (platform, "Timeout", "⚠️")
    except aiohttp.ClientConnectorError:
        return (platform, "Unreachable", "❌")
    except aiohttp.ClientError:
        return (platform, f"Client error", "❗")
    except Exception as e:
        return (platform, f"Error: {str(e)}", "❗")

async def spinner(msg, event):
    for char in itertools.cycle("|/-\\"):
        if event.is_set():
            break
        print(f"\r{msg} {char}", end="", flush=True)
        await asyncio.sleep(0.1)
    print("\r" + " " * (len(msg) + 2) + "\r", end="", flush=True) 

async def main(username):
    platforms = fetch_platforms()
    if not platforms:
        print("⚠️ Could not load platform data.")
        return

    print("─────────────────────────────────────────────")
    print(f"{'Platform':<22} | Status")
    print("─────────────────────────────────────────────")

    stop_spinner = asyncio.Event()

    async with aiohttp.ClientSession() as session:
        spinner_task = asyncio.create_task(spinner("Checking usernames...", stop_spinner))

        tasks = [
            check_username(session, platform, data, username)
            for platform, data in platforms.items()
        ]
        results = await asyncio.gather(*tasks)

        stop_spinner.set()
        await spinner_task

    results.sort(key=lambda x: x[0].lower())

    taken = 0
    available = 0
    warnings = 0

    for platform, status, icon in results:
        print(f"{platform:<22} | {icon} {status}")
        if icon == "✅":
            available += 1
        elif icon == "❌":
            taken += 1
        else:
            warnings += 1

    print("─────────────────────────────────────────────")
    print(f"Summary: {taken} taken, {available} available, {warnings} warnings/errors")
    print("─────────────────────────────────────────────\n")

if __name__ == "__main__":
    username = input("[!] Enter a username to check: ").strip()
    asyncio.run(main(username))
