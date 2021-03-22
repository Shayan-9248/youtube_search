from django.shortcuts import render
from django.views import View
from django.conf import settings
from isodate import parse_duration
import requests


def index(request):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part': 'snippet',
        'q': 'learn django',
        'key': settings.YOUTUBE_DATA_API_KEY,
        'maxResults': 9,
        'type': 'video',
    }

    video_ids = []
    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    for result in results:
        video_ids.append(result['id']['videoId'])

    video_params = {
        'key': settings.YOUTUBE_DATA_API_KEY,
        'part': 'snippet, contentDetails',
        'id': ','.join(video_ids),
        'maxResults': 9,
    }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']

    videos = []
    for result in results:
        video_data = {
            'title': result['snippet']['title'],
            'id': result['id'],
            'duration': parse_duration(result['contentDetails']['duration']).total_seconds() // 60,
            'thumbnail': result['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)
    return render(request, 'youtube/home.html', {'videos': videos})