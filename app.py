from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

API_KEY    = os.getenv("YOUTUBE_API_KEY")
GRADES     = [6, 7, 8, 9, 10]
SUBJECTS   = ["History", "Geography"]
CSV_PATH   = "cbse_cc_videos.csv"
EXCEL_PATH = "cbse_cc_videos.xlsx"


def fetch_cc_videos(api_key: str) -> list[dict]:
    youtube = build("youtube", "v3", developerKey=api_key)
    seen_ids = set()
    data = []

    for grade in GRADES:
        for subject in SUBJECTS:
            search_resp = youtube.search().list(
                q=f"CBSE Class {grade} {subject}",
                part="snippet",
                type="video",
                videoLicense="creativeCommon",
                maxResults=50,
            ).execute()

            video_ids = [
                item["id"]["videoId"]
                for item in search_resp.get("items", [])
                if item["id"]["videoId"] not in seen_ids
            ]

            if not video_ids:
                continue

            details_resp = youtube.videos().list(
                part="snippet,status",
                id=",".join(video_ids)
            ).execute()

            for video in details_resp.get("items", []):
                vid_id = video["id"]
                if vid_id not in seen_ids and video["status"]["license"] == "creativeCommon":
                    seen_ids.add(vid_id)
                    data.append({
                        "Grade":       f"Grade {grade}",
                        "Subject":     subject,
                        "Video Title": video["snippet"]["title"],
                        "Video Link":  f"https://www.youtube.com/watch?v={vid_id}",
                        "License":     "CC BY (Creative Commons)",
                    })

    return data


def main():
    data = fetch_cc_videos(API_KEY)
    df = pd.DataFrame(data)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    df.to_excel(EXCEL_PATH, index=False)


if __name__ == "__main__":
    main()
    print("SuccessFull")