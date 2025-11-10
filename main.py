import csv
import time
import datetime
from telegram_fetcher import fetch_video
from insta_manager import login, upload_reel
from scheduler import today_schedule
from config import csv_file, log_file

cl = login()

def get_next_post():
    with open(csv_file, newline='', encoding='utf-8') as f:
        data = list(csv.DictReader(f))
        for row in data:
            if row["STATUS"] == "PENDING":
                return row
    return None


def mark_as_done(message_id):
    rows = []
    with open(csv_file, newline='', encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        if r["MESSAGE_ID"] == message_id:
            r["STATUS"] = "DONE"

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["SNO","MESSAGE_ID","MESSAGE","VIDEO_NAME","STATUS"])
        writer.writeheader()
        writer.writerows(rows)


def post_cycle():
    schedule_list = today_schedule()

    for post_time in schedule_list:

        print(f"Waiting for {post_time}...")

        # convert to time object
        target = datetime.datetime.strptime(post_time, "%H:%M").time()

        # wait until exact minute
        while True:
            now = datetime.datetime.now().time()
            if now >= target:
                break
            time.sleep(20)

        print("Posting now...")

        row = get_next_post()
        if not row:
            print("No pending posts")
            return

        message_id = int(row["MESSAGE_ID"])

        video_path, caption = cl.loop.run_until_complete(fetch_video(message_id))

        if not video_path:
            print("Error fetching media")
            mark_as_done(row["MESSAGE_ID"])
            continue

        result = upload_reel(video_path, caption)

        if result:
            mark_as_done(row["MESSAGE_ID"])
            print("✅ Post uploaded:", message_id)
        else:
            print("❌ Post failed, will retry next cycle")


while True:
    post_cycle()
    time.sleep(3600)
