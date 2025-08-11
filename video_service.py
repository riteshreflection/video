import yt_dlp
import logging
from urllib.parse import urlparse, parse_qs

def extract_video_data(video_url):
    """
    Extract video data and streaming URLs from YouTube using yt-dlp
    
    Args:
        video_url (str): YouTube video URL
        
    Returns:
        dict: Video metadata and streaming URLs
    """
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # Prefer mp4 format
            'quiet': True,  # Suppress yt-dlp output
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info = ydl.extract_info(video_url, download=False)
            
            # Extract video ID from URL for additional metadata
            video_id = extract_video_id(video_url)
            
            # Prepare streaming formats
            formats = []
            hls_streams = []
            
            if 'formats' in info:
                for fmt in info['formats']:
                    format_data = {
                        'format_id': fmt.get('format_id'),
                        'ext': fmt.get('ext'),
                        'resolution': fmt.get('resolution'),
                        'fps': fmt.get('fps'),
                        'vcodec': fmt.get('vcodec'),
                        'acodec': fmt.get('acodec'),
                        'filesize': fmt.get('filesize'),
                        'url': fmt.get('url'),
                        'quality': fmt.get('quality'),
                        'format_note': fmt.get('format_note')
                    }
                    
                    # Filter out None values
                    format_data = {k: v for k, v in format_data.items() if v is not None}
                    formats.append(format_data)
                    
                    # Collect HLS streams specifically
                    if fmt.get('protocol') == 'm3u8_native' or fmt.get('ext') == 'm3u8':
                        hls_streams.append({
                            'quality': fmt.get('format_note', 'unknown'),
                            'url': fmt.get('url'),
                            'resolution': fmt.get('resolution')
                        })
            
            # Extract thumbnails
            thumbnails = []
            if 'thumbnails' in info:
                for thumb in info['thumbnails']:
                    thumbnails.append({
                        'url': thumb.get('url'),
                        'width': thumb.get('width'),
                        'height': thumb.get('height'),
                        'resolution': thumb.get('resolution')
                    })
            
            # Prepare response data
            video_data = {
                'success': True,
                'video_id': video_id,
                'title': info.get('title'),
                'description': info.get('description'),
                'duration': info.get('duration'),
                'duration_string': info.get('duration_string'),
                'upload_date': info.get('upload_date'),
                'uploader': info.get('uploader'),
                'uploader_id': info.get('uploader_id'),
                'view_count': info.get('view_count'),
                'like_count': info.get('like_count'),
                'thumbnails': thumbnails,
                'webpage_url': info.get('webpage_url'),
                'original_url': video_url,
                'formats': formats,
                'hls_streams': hls_streams,
                'best_video_url': info.get('url'),  # Direct video URL
                'format_count': len(formats)
            }
            
            # Filter out None values from the main response
            video_data = {k: v for k, v in video_data.items() if v is not None}
            
            logging.info(f"Successfully extracted data for video: {info.get('title')}")
            return video_data
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        logging.error(f"yt-dlp download error: {error_msg}")
        
        if 'Video unavailable' in error_msg:
            return {
                'error': 'Video unavailable',
                'message': 'The requested video is not available or has been removed'
            }
        elif 'Private video' in error_msg:
            return {
                'error': 'Private video',
                'message': 'The requested video is private and cannot be accessed'
            }
        elif 'removed by the user' in error_msg:
            return {
                'error': 'Video removed',
                'message': 'The requested video has been removed by the user'
            }
        else:
            return {
                'error': 'Download error',
                'message': f'Unable to extract video data: {error_msg}'
            }
            
    except Exception as e:
        logging.error(f"Unexpected error in video extraction: {str(e)}")
        return {
            'error': 'Extraction failed',
            'message': 'An unexpected error occurred while extracting video data'
        }

def extract_video_id(url):
    """
    Extract video ID from YouTube URL
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: Video ID or None if not found
    """
    try:
        parsed_url = urlparse(url)
        
        if 'youtube.com' in parsed_url.netloc:
            if 'watch' in parsed_url.path:
                return parse_qs(parsed_url.query).get('v', [None])[0]
        elif 'youtu.be' in parsed_url.netloc:
            return parsed_url.path.lstrip('/')
            
        return None
    except:
        return None
