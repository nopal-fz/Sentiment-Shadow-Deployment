import os
import csv
import logging
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 
API_KEY = os.getenv("API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

# Functioon to get comments for a video
def get_video_comments(video_id, max_comments=200):
    comments = []
    next_page_token = None

    logging.info(f"Fetching comments for video: {video_id}")

    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=1000,  # max limit
            textFormat="plainText",
            pageToken=next_page_token
        ).execute()

        for item in response["items"]:
            if len(comments) >= max_comments:
                break

            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "video_id": video_id,
                "author": snippet["authorDisplayName"],
                "comment": snippet["textDisplay"],
                "likes": snippet["likeCount"],
                "published_at": snippet["publishedAt"]
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    logging.info(f"Collected {len(comments)} comments for {video_id}")
    return comments

# Function to save comments to CSV
def save_comments(video_id, comments, category, period):
    folder = f"data/raw/{category}/{period}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/{video_id}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "video_id",
                "author",
                "comment",
                "likes",
                "published_at",
                "category",
                "period"
            ]
        )

        writer.writeheader()

        for row in comments:
            row["category"] = category
            row["period"] = period
            writer.writerow(row)

    logging.info(f"Saved file: {filename}")

# Main function to scrape videos and
def scrape_videos(video_dict, comments_per_video=200):
    """
    video_dict format:
    {
        "podcast": {
            "old": [...],
            "new": [...]
        },
        "gaming": {
            "old": [...],
            "new": [...]
        }
    }
    """

    for category, periods in video_dict.items():
        logging.info(f"Processing category: {category}")

        for period, video_ids in periods.items():
            logging.info(f"  Period: {period}")

            for vid in video_ids:
                try:
                    comments = get_video_comments(vid, comments_per_video)
                    save_comments(vid, comments, category, period)

                except Exception as e:
                    logging.error(f"Error on video {vid}: {e}")

# Parse video IDs from URLs
def extract_video_ids(urls):
    """
    Extract YouTube video IDs from various URL formats.
    Supports:
    - youtube.com/watch?v=
    - youtu.be/
    - youtube.com/shorts/
    - youtube.com/embed/
    - direct video ID
    """
    video_ids = []

    for url in urls:
        try:
            # kalau langsung ID
            if len(url) == 11 and "/" not in url:
                video_ids.append(url)
                continue

            parsed = urlparse(url)

            # youtube.com/watch?v=
            if "youtube.com" in parsed.netloc:
                query = parse_qs(parsed.query)

                if "v" in query:
                    video_ids.append(query["v"][0])
                elif "/shorts/" in parsed.path:
                    video_ids.append(parsed.path.split("/shorts/")[1])
                elif "/embed/" in parsed.path:
                    video_ids.append(parsed.path.split("/embed/")[1])

            # youtu.be/xxxx
            elif "youtu.be" in parsed.netloc:
                video_ids.append(parsed.path.strip("/"))

        except Exception as e:
            print(f"Error parsing URL {url}: {e}")

    return video_ids

# Example video dictionary
video_dict = {
    "podcast": {
        "old": extract_video_ids([
            "https://www.youtube.com/watch?v=2CN-prcBP5Y",
            "https://www.youtube.com/watch?v=ZMRzWwXdgio",
            "https://www.youtube.com/watch?v=CK7L4-dS4OA"
        ]),
        "new": extract_video_ids([
            "https://www.youtube.com/watch?v=XDT2N2_8kTU",
            "https://www.youtube.com/watch?v=brN3TZwyQJU",
            "https://www.youtube.com/watch?v=pC4d8SmFQI8"
        ])
    },
    "gaming": {
        "old": extract_video_ids([
            "https://www.youtube.com/watch?v=zi8oi8B2I9E",
            "https://www.youtube.com/watch?v=hzUG58aJ124",
            "https://www.youtube.com/watch?v=-KV2s-N_Ay4"
        ]),
        "new": extract_video_ids([
            "https://www.youtube.com/watch?v=vIy2Xs0jEhE",
            "https://www.youtube.com/watch?v=oNWGpVpBGsk",
            "https://www.youtube.com/watch?v=2kfmi_U2sVI"
        ])
    }
}

# Run the scraper
if __name__ == "__main__":
    scrape_videos(video_dict, comments_per_video=1000)