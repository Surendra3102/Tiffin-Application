from django.contrib import admin
from .models import MenuItem, Order, OrderItem

# -------------------------
# Menu Item Admin
# -------------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)


# -------------------------
# Order Item Inline
# -------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# -------------------------
# Order Admin
# -------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
