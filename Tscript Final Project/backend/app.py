from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/|v\/|youtu.be\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        return "Invalid YouTube URL. Could not extract video ID."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        if "Subtitles are disabled" in str(e):
            return "Transcripts are disabled for this video."
        elif "No transcripts were found" in str(e):
            return "No transcript found for this video."
        else:
            return f"An error occurred: {str(e)}"

@app.route('/get_transcript', methods=['POST'])
def get_transcript_route():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    transcript = get_transcript(video_url)
    if "error" in transcript.lower():
        response = jsonify({"error": transcript})
        response.status_code = 400
    else:
        response = jsonify({"transcript": transcript})
    
    print(response.get_data(as_text=True))  # Log the response
    
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)