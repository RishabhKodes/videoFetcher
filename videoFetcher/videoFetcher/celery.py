import os
from celery import Celery
from dateutil import parser
from youtube_search.models import Video
import requests
from django.conf import settings
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videoFetcher.settings")

app = Celery("videoFetcher") # defining the app name for celery

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

logger = get_task_logger(__name__)


# Defining the task that fetches the youtube video data peridically through the YT api

@app.task(bind=True)
def videoSearch(self):

    search_url = settings.YOUTUBE_SEARCH_URL
    
    # setting the time according to rfc 3339 format
    time_difference = (datetime.now() - timedelta(minutes=settings.TIME_INTERVAL)).isoformat()


    # Fetching the video data from the YT api (calling the parameters below)
    search_params = {
            'part' : settings.SEARCH_PARAM_PART,
            'q' : settings.SEARCH_PARAM_QUERY,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : settings.SEARCH_PARAM_MAX_RESULTS,
            'order': settings.SEARCH_PARAM_ORDER,
            'type' : settings.SEARCH_PARAM_TYPE,
            'publishedAfter' : time_difference[0:19]+'Z'  # defining time difference of 60 seconds to get the videos published after the time difference
        }

    r = requests.get(search_url, params=search_params)
    
    # Parsing the json data from the YT api
    search_response = r.json()

    print("Received "+str(len(search_response))+" more videos.")

    for item in search_response.get("items", []):

        '''
            Make sure no duplicate videos are added to the database, checking that 
            with the condition below using the video id.
        '''

        if all([not Video.objects.filter(video_link=item["id"]["videoId"]).exists(),
            item["id"]["kind"] == "youtube#video",]):

        # getting esssential data from the json as per the db schema
            video = Video(
                id=item["id"]["videoId"],
                title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                published_on=parser.parse(item["snippet"]["publishedAt"]),
                thumbnail_url=item["snippet"]["thumbnails"]["default"]["url"],
                video_link=settings.BASE_URL +item["id"]["videoId"],
            )
            video.save()  # saving the video to the database
    logger.info("Video database updated at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
