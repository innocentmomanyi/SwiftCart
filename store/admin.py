from django.contrib import admin

from .models import (
    Category,
    Product,
    Cart,
    Order,
    OrderItem,
    Review,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'brand',
        'price',
        'stock',
        'available',
    )

    list_filter = (
        'category',
        'available',
    )

    search_fields = (
        'name',
        'brand',
    )

    ordering = (
        'name',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'created_at',
    )

    search_fields = (
        'user__username',
        'product__name',
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'user__username',
    )

    inlines = [
        OrderItemInline
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'product',
        'user',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'product__name',
        'user__username',
    )