from flask import request, jsonify
from app import app
from video_service import extract_video_data
import logging

@app.route('/')
def index():
    """API service information"""
    return jsonify({
        'service': 'YouTube Video Data Extraction API',
        'version': '1.0.0',
        'description': 'Extract video metadata and streaming URLs from YouTube videos',
        'usage': 'GET /video?url=https://www.youtube.com/watch?v=VIDEO_ID',
        'example': f'{request.host_url}video?url=https://www.youtube.com/watch?v=Nl-GCrDypNY'
    })

@app.route('/video', methods=['GET'])
def get_video_data():
    """
    Extract YouTube video data and streaming URLs
    
    Parameters:
    - url: YouTube video URL (required)
    
    Returns:
    JSON response with video metadata and streaming URLs
    """
    try:
        # Get YouTube URL from query parameters
        video_url = request.args.get('url')
        
        if not video_url:
            return jsonify({
                'error': 'Missing required parameter: url',
                'message': 'Please provide a YouTube URL using the url parameter'
            }), 400
        
        # Validate that it's a YouTube URL
        if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
            return jsonify({
                'error': 'Invalid URL',
                'message': 'Please provide a valid YouTube URL'
            }), 400
        
        # Extract video data using yt-dlp
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
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'YouTube Video Data Extraction Server',
        'version': '1.0.0'
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500
