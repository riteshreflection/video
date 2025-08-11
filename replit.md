# YouTube Video Data Extraction API

## Overview

This is a Flask-based REST API that extracts video metadata and streaming URLs from YouTube videos using yt-dlp. The application provides a simple HTTP endpoint that accepts YouTube URLs and returns detailed video information including available streaming formats, quality options, and metadata. It serves both as a programmatic API and includes a web-based documentation interface for easy testing and exploration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **API Design**: RESTful API with a single GET endpoint `/video` that accepts YouTube URLs as query parameters
- **Service Layer**: Dedicated `video_service.py` module that handles YouTube data extraction using yt-dlp
- **Error Handling**: Comprehensive error handling with structured JSON responses for different failure scenarios
- **Cross-Origin Support**: CORS enabled for browser-based requests

### Request/Response Flow
- Client sends GET request with YouTube URL as query parameter
- Server validates URL format to ensure it's a valid YouTube link
- yt-dlp extracts video metadata without downloading the actual video file
- Response includes video details, multiple streaming format options, and quality information
- Errors are returned as structured JSON with appropriate HTTP status codes

### API Interface
- **Simple JSON API**: Pure REST API service without web interface
- **Browser-friendly**: JSON responses can be viewed directly in browser
- **Lightweight**: Minimal overhead for maximum performance

### Configuration Management
- Environment-based configuration for session secrets
- Development-friendly defaults with debug mode enabled
- Configurable host and port settings for deployment flexibility

## External Dependencies

### Core Libraries
- **Flask**: Web framework for API endpoints and request handling
- **flask-cors**: Cross-origin resource sharing support for browser requests
- **yt-dlp**: YouTube video data extraction and format parsing
- **gunicorn**: Production WSGI server for deployment

### Runtime Requirements
- Python 3.11+ environment
- No database dependencies - stateless API design
- No authentication system - open access API

## Deployment

### Files Created for Deployment
- **requirements.txt**: Python dependencies for external hosting
- **render.yaml**: Render.com deployment configuration
- **README.md**: Project documentation and API usage guide
- **DEPLOYMENT.md**: Step-by-step deployment instructions
- **.gitignore**: Git ignore rules for clean repository

### Deployment Platforms
- **Primary**: Render.com (configured with render.yaml)
- **Alternative**: Heroku, Railway, or any Python hosting service
- **Local Development**: Flask development server on port 5000