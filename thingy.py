import subprocess

OUTPUT_FILE = "vimeo-video(current2)-fast.ts"


def download_video():
    url = input("\nPaste your Vimeo URL: ").strip()
    url = url.replace("\ufeff", "").replace("\u200b", "").replace(" ", "")

    if not url:
        print("No URL provided.")
        return

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    command = [
        "streamlink",
        "--http-header", "User-Agent=Mozilla/5.0",
        "--http-header", "Referer=https://player.vimeo.com/",
        "--stream-segment-threads", "8",
        "--output", OUTPUT_FILE,
        url,
        "360p"
    ]

    try:
        subprocess.run(command, check=False)
    except FileNotFoundError:
        print("Error: Streamlink was not found. Make sure it's installed and in PATH.")


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
        print("1. Download")
        print("2. Change name")
        print("3. Exit")

        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            download_video()
            input("\nPress Enter to continue...")
        elif choice == "2":
            change_name()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

