from django.contrib import admin
from .models import MenuItem, Order, OrderItem
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)  
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)  # Assuming you want to search by username
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity')
    list_filter = ('order', 'menu_item')
    search_fields = ('order__user__username', 'menu_item__name')  # Assuming you want to search by username and menu item name
    
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
