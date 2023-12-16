from django.contrib import admin
from .models import Order, OrderBook


class OrderBookInline(admin.TabularInline):
    model = OrderBook
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner', 'status', 'due_time', 'formatted_created_time')
    inlines = [OrderBookInline]


admin.site.register(Order, OrderAdmin)
