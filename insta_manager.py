from instagrapi import Client
import time
from config import instagram_session_json, username

cl = Client()

def login():
    try:
        cl.load_settings(instagram_session_json)
        cl.login(username, "unused_password_because_session")
    except:
        cl.login(username, input("Enter Password: "))
        cl.dump_settings(instagram_session_json)

    return cl


def upload_reel(video_path, caption):
    try:
        cl.clip_upload(video_path, caption)
        return True
    except Exception as e:
        print("Upload Error:", e)
        return False
