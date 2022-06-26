import os
from celery import Celery
from dateutil import parser
from youtube_search.models import Video
import requests
from django.conf import settings
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videoFetcher.settings")

app = Celery("videoFetcher")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

@app.task(bind=True)
def hello_world(self):
    print("Hello world!")

logger = get_task_logger(__name__)


@app.task(bind=True)
def videoSearch(self):

    search_url = settings.YOUTUBE_SEARCH_URL
    
    time_difference = (datetime.now() - timedelta(minutes=settings.TIME_INTERVAL)).isoformat()

    search_params = {
            'part' : settings.SEARCH_PARAM_PART,
            'q' : settings.SEARCH_PARAM_QUERY,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : settings.SEARCH_PARAM_MAX_RESULTS,
            'order': settings.SEARCH_PARAM_ORDER,
            'type' : settings.SEARCH_PARAM_TYPE,
            # 'publishedAfter' : time_difference[0:19]+'Z'
        }

    r = requests.get(search_url, params=search_params)
        
    search_response = r.json()

    print("Received "+str(len(search_response))+" more videos.")

    for item in search_response.get("items", []):
        if all([not Video.objects.filter(link=item["id"]["videoId"]).exists(),
            item["id"]["kind"] == "youtube#video",]):

            video = Video(
                id=item["id"]["videoId"],
                video_title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                published_on=parser.parse(item["snippet"]["publishedAt"]),
                thumb_url=item["snippet"]["thumbnails"]["default"]["url"],
                link=settings.BASE_URL +item["id"]["videoId"],
            )
            video.save()
    logger.info("Video database updated at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
