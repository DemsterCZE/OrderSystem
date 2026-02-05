from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, MenuItem, Table, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_item_price',)
    fields = ('item', 'quantity', 'total_item_price')


# Registrace objednávek
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'table_id',
        'assigned_employee',
        'display_actual_status',
        'display_total_order_price',
        'order_time',
        'accepted_time',
        'completed_time',
    )

    list_filter = ('order_status', 'table_id', 'order_time')

    search_fields = ('order_id', 'table_id__table_name')

    inlines = [OrderItemInline]

    def display_actual_status(self, obj):
        return obj.get_actual_order_status()

    display_actual_status.short_description = 'Aktuální stav'

    def display_total_order_price(self, obj):
        return f"{obj.get_total_order_price()} Kč"

    display_total_order_price.short_description = 'Celková cena'


# Registrace Menu
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'category_name')
    search_fields = ('item_name', 'category')

    def category_name(self, obj):
        return obj.get_category_name()

    category_name.short_description = 'Typ položky'


# Registrace stolů
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_name',)


# Registrace zaměstnanců
@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    list_display_links = ('id', 'username')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name')}),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Osobní údaje', {'fields': ('first_name', 'last_name')}),
    )
