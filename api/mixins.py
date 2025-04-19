from rest_framework import mixins, viewsets


class ListMixin(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
