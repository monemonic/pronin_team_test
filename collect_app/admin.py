from django.contrib import admin

from .models import CollectType, Collect, Payment


@admin.register(CollectType)
class CollectTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'collect_target', 'collection_end_date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'donater', 'collect')
