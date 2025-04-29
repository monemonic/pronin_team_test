from django.core.cache import cache
from django.db.models import Count, Prefetch, Sum

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import CreateMixin, ListMixin
from api.permissions import IsAuthorOrReadOnly
from collect_app.collect_swaggers import (COLLECT_SWAGGER,
                                          COLLETCT_TYPE_SWAGGER,
                                          PAYMENT_SWAGGER)
from collect_app.constants import COLLECT_CONSTANTS
from collect_app.models import Collect, CollectType, Payment
from utils_app.services import BaseService

from .paginations import CollectListPageNumberPagination
from .serializers import (CollectSerializer, CollectTypeSerializer,
                          PaymentSerializer, ReadCollectSerializer)


@extend_schema(tags=['Поводы сбора'])
class CollectTypeViewSet(ListMixin):
    queryset = CollectType.objects.all()
    serializer_class = CollectTypeSerializer

    @COLLETCT_TYPE_SWAGGER['list']
    def list(self, request, *args, **kwargs):
        cached_data = cache.get(COLLECT_CONSTANTS['CACHE_COLLECT_TYPE_LIST'])
        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(
                COLLECT_CONSTANTS['CACHE_COLLECT_TYPE_LIST'],
                response.data,
                timeout=COLLECT_CONSTANTS['CACHE_COLLECT_TYPE_LIST_lIFE_TIME']
            )
            return response

        return Response(cached_data)


@extend_schema(tags=['Сборы'])
class CollectViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = CollectListPageNumberPagination

    def get_serializer_class(self):
        match self.action:
            case 'create' | 'partial_update':
                return CollectSerializer
            case _:
                return ReadCollectSerializer

    def get_permissions(self):
        match self.action:
            case 'create':
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
        """
        Создание кверисета для работы с групповыми сборами
        """
        count_donaters = Count('payments__donater', distinct=True)
        payments = Prefetch(
            'payments',
            queryset=Payment.objects.all().select_related('donater')
        )
        amount_collected = Sum('payments__amount')
        queryset = Collect.objects.all().prefetch_related(
            payments
        ).select_related('collect_type').annotate(
            count_donaters=count_donaters,
            amount_collected=amount_collected
        ).order_by('-created_at')
        return queryset

    @COLLECT_SWAGGER['create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @COLLECT_SWAGGER['partial_update']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @COLLECT_SWAGGER['destroy']
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @COLLECT_SWAGGER['list']
    def list(self, request, *args, **kwargs):
        # Параметры запроса для создания ключа кеша
        page_num = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '')

        # Генерация ключа кеша
        key = f'{page_num}:{page_size}'
        generate_key = BaseService.generate_cache_key(key)

        cached_key = COLLECT_CONSTANTS['CACHE_COLLECTS_LIST'].format(
            params=generate_key
        )

        cached_data = cache.get(cached_key)

        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(
                cached_key, response.data,
                timeout=COLLECT_CONSTANTS['CACHE_COLLECTS_LIST_LIFE_TIME']
            )
            return response

        return Response(cached_data)

    @COLLECT_SWAGGER['retrieve']
    def retrieve(self, request, *args, **kwargs):

        generate_key = BaseService.generate_cache_key(self.kwargs['pk'])

        cached_key = COLLECT_CONSTANTS['CACHE_RETRIEVE_COLLECT'].format(
            collect_id=generate_key
        )
        cached_data = cache.get(cached_key)
        if cached_data is None:
            response = super().retrieve(request, *args, **kwargs)
            cache.set(
                cached_key,
                response.data,
                timeout=COLLECT_CONSTANTS['CACHE_RETRIEVE_COLLECT_LIFE_TIME']
            )
            return response

        return Response(cached_data)


@extend_schema(tags=['Пожертвования'])
class PaymentViewSet(CreateMixin):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(donater=self.request.user)

    @PAYMENT_SWAGGER['create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
