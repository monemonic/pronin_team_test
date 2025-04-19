from django.db.models import Count, Prefetch, Sum
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import ListMixin
from api.permissions import IsAuthorOrReadOnly
from collect_app.constants import COLLECT_CONSTANTS
from collect_app.models import Collect, CollectType, Payment
from collect_app.collect_swaggers import COLLECT_SWAGGER, COLLETCT_TYPE_SWAGGER
from utils_app.services import BaseService

from .paginations import CollectListPageNumberPagination
from .serializers import (CollectSerializer, CollectTypeSerializer,
                          PaymentSerializer, ReadCollectSerializer)


@extend_schema(tags=['Поводы сбора'])
class CollectTypeViewSet(ListMixin):
    queryset = CollectType.objects.all()
    serializer_class = CollectTypeSerializer

    @BaseService.cache_response_decorator(
        COLLECT_CONSTANTS['CACHE_COLLECT_TYPE_LIST'],
        COLLECT_CONSTANTS['CACHE_COLLECT_TYPE_LIST_lIFE_TIME']
    )
    @COLLETCT_TYPE_SWAGGER['list']
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=['Сборы'])
class CollectViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = CollectListPageNumberPagination

    def get_serializer_class(self):
        match self.action:
            case 'create' | 'partial_update':
                return CollectSerializer
            case 'add_donate':
                return PaymentSerializer
            case _:
                return ReadCollectSerializer

    def get_permissions(self):
        match self.action:
            case 'add_donate' | 'create':
                return (IsAuthenticated(),)
            case _:
                return (IsAuthorOrReadOnly(),)

    def perform_create(self, serializer):
        """
        Устанавливает текущего аутентифицированного пользователя автора
        сбора при создании.
        """
        serializer.save(author=self.request.user)

    def get_queryset(self):
        count_donaters = Count('payments__donater', distinct=True)
        payments = Prefetch(
            'payments',
            queryset=Payment.objects.all().select_related('donater')
        )
        amount_collected = Sum('payments__amount')
        return Collect.objects.all().prefetch_related(
            payments
        ).select_related('collect_type').annotate(
            count_donaters=count_donaters,
            amount_collected=amount_collected
        ).order_by('-id')

    @COLLECT_SWAGGER['add_donate']
    @action(detail=True, methods=['post'])
    def add_donate(self, request, pk):
        """
        Создание нового пожертвования для указанного сбора
        """
        collect = get_object_or_404(Collect, pk=pk)
        self.check_object_permissions(request, collect)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(collect=collect, donater=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @COLLECT_SWAGGER['create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @COLLECT_SWAGGER['partial_update']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @COLLECT_SWAGGER['destroy']
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def _generate_cache_key_list_collects(self, request, *args, **kwargs):
        """Метод создания ключа кеша для списка сборов"""

        # Параметры запроса для создания ключа кеша
        page_num = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '')

        # Генерация ключа кеша
        key = f'{page_num}:{page_size}'
        generate_key = BaseService.generate_cache_key(key)

        cached_key = COLLECT_CONSTANTS['CACHE_COLLECTS_LIST'].format(
            params=generate_key
        )
        return cached_key

    @BaseService.cache_response_decorator(
        _generate_cache_key_list_collects,
        COLLECT_CONSTANTS['CACHE_COLLECTS_LIST_LIFE_TIME']
    )
    @COLLECT_SWAGGER['list']
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def _generate_cache_key_retrieve_collect(self, request, *args, **kwargs):
        """Метод создания ключа кеша для списка сборов"""

        # Получение ID сбора для генерации ключа
        collect_id = self.kwargs['pk']

        # Генерация ключа кеша
        key = f'{collect_id}'
        generate_key = BaseService.generate_cache_key(key)

        cached_key = COLLECT_CONSTANTS['CACHE_RETRIEVE_COLLECT'].format(
            collect_id=generate_key
        )
        return cached_key

    @BaseService.cache_response_decorator(
        _generate_cache_key_retrieve_collect,
        COLLECT_CONSTANTS['CACHE_RETRIEVE_COLLECT_LIFE_TIME']
    )
    @COLLECT_SWAGGER['retrieve']
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
