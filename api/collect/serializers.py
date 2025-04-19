from rest_framework import serializers

from api.user.serializers import ReadMiniUserSerializer
from collect_app.models import Collect, CollectType, Payment
from utils_app.services import Base64ImageField


class CollectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectType
        fields = ('id', 'name')


class CollectSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Collect
        fields = (
            'id', 'author', 'name',
            'collect_type', 'description', 'description', 'collect_target',
            'image', 'collection_end_date'
        )
        read_only_fields = ('author',)


class PaymentSerializer(serializers.ModelSerializer):
    donater = ReadMiniUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M', read_only=True
    )

    class Meta:
        model = Payment
        fields = ('id', 'donater', 'amount', 'created_at')


class ReadCollectSerializer(CollectSerializer):
    collect_type = CollectTypeSerializer()
    count_donaters = serializers.IntegerField(read_only=True)
    payments = PaymentSerializer(many=True)
    amount_collected = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collect
        fields = CollectSerializer.Meta.fields + (
            'count_donaters', 'amount_collected', 'payments'
        )
