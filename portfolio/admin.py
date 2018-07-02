from django.contrib import admin
from django.contrib.auth.models import User
from .models import Service, ServiceStatus
from .utils import user_is_group_member


# Услуги
class ServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'status', 'manager', 'description')
        }),
        ('Аналитичекие показатели', {
            'fields': ('customer', 'price', 'costs', 'importance', 'value')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at', 'notes')
        })
    )
    list_display = ('name', 'status', 'manager', 'value', 'created_at', 'updated_at')
    list_filter = ('status', 'manager')
    ordering = ('created_at', 'value')
    search_fields = ('name', )

    #autocomplete_fields = ('manager', )

    # Настройка полей формы
    def get_form(self, request, obj=None, **kwargs):
        # Супер пользователь
        if request.user.is_superuser:
            self.readonly_fields = tuple('value')
        # Менеджер
        elif user_is_group_member(request.user, 'Менеджер'):
            self.readonly_fields = tuple('value')
        # Остальные пользователи
        else:
            self.readonly_fields = ('created_at', 'manager', 'value')
        return super(ServiceAdmin, self).get_form(request, obj, **kwargs)

    # Сохранение модели
    def save_model(self, request, obj, form, change):
        # Автоматическое назначение менеджера при добавлении услуги
        if not hasattr(obj, 'manager'):
            obj.manager = request.user
        if obj.price > 0 and obj.costs > 0 and obj.importance != 0:
            value = obj.price / obj.costs * obj.importance
            obj.value = round(value)
        return super().save_model(request, obj, form, change)

admin.site.register(Service, ServiceAdmin)


# Статусы услуг
class ServiceStatusAdmin(admin.ModelAdmin):

    # Доступ к модулю статусов услуг может иметь только администратор или менеджер
    def has_module_permission(self, request):
        return request.user.is_superuser or user_is_group_member(request.user, 'Менеджер')

    # Добавлять статусы услуг может только администратор или менеджер
    def has_create_permission(self, request, obj=None):
        return request.user.is_superuser or user_is_group_member(request.user, 'Менеджер')

    # Удолять статусы услуг может только администратор или менеджер
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or user_is_group_member(request.user, 'Менеджер')

    # Изменять статусы услуг может только администратор или менеджер
    def has_cahnge_permission(self, request, obj=None):
        return request.user.is_superuser or user_is_group_member(request.user, 'Менеджер')



admin.site.register(ServiceStatus, ServiceStatusAdmin)


# Пользователи
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'email', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
