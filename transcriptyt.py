import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
# Set up the video URL
video_url = "https://youtu.be/xxVk4DeDHbI?feature=shared"

# Extract the video ID from the URLcl
match = re.findall(r"youtu.be/([^?]+)", video_url)
if match:
    video_id = match[0]
else:
    print("Error: Unable to extract video ID from the URL.")
    exit()

# Try to get the transcript of the video
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
except TranscriptsDisabled:
    print("Error: Could not retrieve a transcript for this video because subtitles are disabled.")
    exit()
