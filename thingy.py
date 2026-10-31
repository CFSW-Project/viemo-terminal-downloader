
import subprocess
import os
import re

OUTPUT_FILE = "vimeo-video(current2)-fast.ts"
VIDEO_QUALITY = "best"


def get_url():
    print("\nPaste your Vimeo URL (up to 6 lines).")
    print("Press Enter twice when finished:\n")

    lines = []

    while len(lines) < 6:
        try:
            line = input()
        except EOFError:
            break

        if not line.strip():
            if lines:
                break
            continue

        lines.append(line.strip())

    url = "".join(lines)
    url = url.replace("\ufeff", "").replace("\u200b", "")
    url = url.strip()

    if not url:
        print("\nNo URL provided.")
        return None

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    return url


def check_qualities(url):
    print("\nChecking available qualities for this URL...\n")

    command = [
        "streamlink",
        "--http-header", "User-Agent=Mozilla/5.0",
        "--http-header", "Referer=https://player.vimeo.com/",
        url
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace"
        )

        output = result.stdout + "\n" + result.stderr

        if result.returncode != 0:
            print(output)
            print("\nCould not retrieve available streams.")
            print("Check the URL, Vimeo permissions, or Streamlink version.")
            return None

        match = re.search(
            r"Available streams:\s*(.*)",
            output,
            re.IGNORECASE
        )

        if not match:
            print(output)
            print("\nNo available quality list was detected.")
            return None

        streams_text = match.group(1).strip()

        qualities = [
            q.strip()
            for q in streams_text.split(",")
            if q.strip()
        ]

        if not qualities:
            print("\nNo qualities found.")
            return None

        print("================================")
        print("       AVAILABLE QUALITIES")
        print("================================")

        for i, quality in enumerate(qualities, 1):
            print(f"{i}. {quality}")

        print("================================")

        return qualities

    except FileNotFoundError:
        print("\nStreamlink was not found.")
        print("Install it using: pip install streamlink")
        return None


def choose_quality(qualities):
    global VIDEO_QUALITY

    print("\nSelect your preferred quality:")

    for i, quality in enumerate(qualities, 1):
        current = " <-- CURRENT" if quality == VIDEO_QUALITY else ""
        print(f"{i}. {quality}{current}")

    print("B. Best available")
    print("C. Cancel")

    choice = input("\nChoose an option: ").strip()

    if choice.lower() == "c":
        return None

    if choice.lower() == "b":
        VIDEO_QUALITY = "best"
        return VIDEO_QUALITY

    try:
        index = int(choice) - 1

        if 0 <= index < len(qualities):
            VIDEO_QUALITY = qualities[index]
            return VIDEO_QUALITY

    except ValueError:
        pass

    print("\nInvalid selection.")
    return choose_quality(qualities)


def download_video():
    url = get_url()

    if not url:
        return

    qualities = check_qualities(url)

    if not qualities:
        return

    selected = choose_quality(qualities)

    if not selected:
        print("\nDownload cancelled.")
        return

    print(f"\nStarting download...")
    print(f"Quality: {selected}")
    print(f"Output: {OUTPUT_FILE}")

    command = [
        "streamlink",
        "--http-header", "User-Agent=Mozilla/5.0",
        "--http-header", "Referer=https://player.vimeo.com/",
        "--stream-segment-threads", "9",
        "--retry-streams", "3",
        "--retry-max", "5",
        "--output", OUTPUT_FILE,
        url,
        selected
    ]

    try:
        result = subprocess.run(command, check=False)

        if result.returncode == 0:
            print(f"\nDownload completed: {OUTPUT_FILE}")
        else:
            print("\nDownload failed.")
            print("Check the URL, selected quality, or Vimeo permissions.")

    except FileNotFoundError:
        print("\nError: Streamlink was not found.")
        print("Install it using: pip install streamlink")


def change_name():
    global OUTPUT_FILE

    new_name = input("\nEnter the new output filename: ").strip()

    if not new_name:
        print("No filename provided.")
        return

    if not new_name.lower().endswith(".ts"):
        new_name += ".ts"

    OUTPUT_FILE = new_name
    print(f"\nFuture downloads will be saved as: {OUTPUT_FILE}")


def main():
    while True:
        print("\n==============================")
        print("       VIMEO DOWNLOADER")
        print("==============================")
        print("1. Download video")
        print("2. Change filename")
        print("3. Exit")

        print(f"\nCurrent filename: {OUTPUT_FILE}")
        print(f"Preferred quality: {VIDEO_QUALITY}")

        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            download_video()
            input("\nPress Enter to continue...")

        elif choice == "2":
            change_name()
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

