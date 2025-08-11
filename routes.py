from flask import Flask, request, jsonify
import os
import logging
from video_service import extract_video_data, write_cookies_file

app = Flask(__name__)

# Write cookies.txt on app startup from env var
write_cookies_file()

@app.route('/')
def index():
    return jsonify({
        'service': 'YouTube Video Data Extraction API',
        'version': '1.0.0',
        'description': 'Extract video metadata and streaming URLs from YouTube videos',
        'usage': 'GET /video?url=https://www.youtube.com/watch?v=VIDEO_ID',
        'example': f'{request.host_url}video?url=https://www.youtube.com/watch?v=Nl-GCrDypNY'
    })

@app.route('/video', methods=['GET'])
def get_video_data():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({
            'error': 'Missing required parameter: url',
            'message': 'Please provide a YouTube URL using the url parameter'
        }), 400

    if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
        return jsonify({
            'error': 'Invalid URL',
            'message': 'Please provide a valid YouTube URL'
        }), 400

    try:
        video_data = extract_video_data(video_url)
        if video_data.get('error'):
            return jsonify(video_data), 404
        return jsonify(video_data), 200
    except Exception as e:
        logging.error(f"Error processing video request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An error occurred while processing the video URL'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'YouTube Video Data Extraction Server',
        'version': '1.0.0'
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
