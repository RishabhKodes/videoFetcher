from rest_framework.decorators import api_view
from youtube_search.models import Video
from django.conf import settings
from youtube_search.serializers import VideoSerializer
from .pagination import StandardResultsSetPagination


@api_view(['GET'])
def getVideos(request):
    pagination = StandardResultsSetPagination()
    query_set = Video.objects.all()
    context = pagination.paginate_queryset(query_set, request)
    serializer = VideoSerializer(context, many=True)
    return pagination.get_paginated_response(serializer.data)


# @api_view(['GET'])
# def getData(request):
#     items = Item.objects.all()
#     serializer = ItemSerializer(items, many=True)
#     return  Response(serializer.data)
