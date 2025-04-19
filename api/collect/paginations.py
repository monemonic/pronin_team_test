from rest_framework.pagination import PageNumberPagination

from collect_app.constants import COLLECT_CONSTANTS


class CollectListPageNumberPagination(PageNumberPagination):
    page_size = COLLECT_CONSTANTS['PAGE_SIZE_LIST_COLLECT']
    page_size_query_param = 'page_size'
    max_page_size = COLLECT_CONSTANTS['MAX_PAGE_SIZE_LIST_COLLECT']
