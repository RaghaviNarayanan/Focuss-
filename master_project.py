import threading
import time
from yolov1 import run_focusai_combined
# from send_summary import run_summary_email  # Optional: include if you want a daily report

def main():
    print("🚀 Launching Focus...")

    # Run combined face + phone detection in one thread
    combined_thread = threading.Thread(target=run_focusai_combined)
    combined_thread.start()

    # Optional: Add summary email after a delay or at end
    # summary_thread = threading.Thread(target=run_summary_email)
    # summary_thread.start()

    try:
        while combined_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n❌ Stopped by user")

if __name__ == "__main__":
    main()
