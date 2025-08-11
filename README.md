# YouTube Video Data Extraction API

A simple Flask-based REST API that extracts video metadata and streaming URLs from YouTube videos using yt-dlp.

## Features

- 🎥 Extract video metadata (title, description, duration, etc.)
- 📺 Get HLS streaming URLs for different quality options
- 🖼️ Retrieve thumbnail information
- 📊 Multiple video format support (MP4, WebM, etc.)
- 🔗 Simple REST API interface

## API Endpoints

### GET /
Returns basic API information and usage instructions.

### GET /video?url={youtube_url}
Extracts video data from a YouTube URL.

**Parameters:**
- `url` (required): YouTube video URL (youtube.com or youtu.be)

**Example:**
```
GET /video?url=https://www.youtube.com/watch?v=Nl-GCrDypNY
```

**Response:**
```json
{
  "success": true,
  "video_id": "Nl-GCrDypNY",
  "title": "Video Title",
  "description": "Video description...",
  "duration": 180,
  "duration_string": "3:00",
  "uploader": "Channel Name",
  "view_count": 1000000,
  "thumbnails": [...],
  "formats": [...],
  "hls_streams": [...],
  "best_video_url": "https://..."
}
```

### GET /health
Health check endpoint to verify service status.

## Deployment

### Deploy to Render

1. Fork this repository to your GitHub account
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Select this repository
5. Render will automatically detect the `render.yaml` configuration
6. Deploy!

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd youtube-video-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## Environment Variables

- `SESSION_SECRET`: Flask session secret key (auto-generated on Render)
- `PORT`: Server port (automatically set by Render)

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Video Processing**: yt-dlp (YouTube data extraction)
- **CORS**: flask-cors (Cross-origin resource sharing)
- **Server**: Gunicorn (WSGI HTTP server)

## Error Handling

The API provides comprehensive error handling for:
- Invalid URLs
- Private or unavailable videos
- Network issues
- Extraction failures

All errors return structured JSON responses with appropriate HTTP status codes.

## License

MIT License - feel free to use this project for your own purposes.