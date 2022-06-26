from rest_framework import pagination

# setting the pagination for the api according to 10 results per page

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 10