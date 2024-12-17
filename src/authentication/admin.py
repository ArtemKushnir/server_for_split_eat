from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_active", "is_superuser", "is_staff", "date_joined")  # Поля для отображения
    list_filter = ("is_active", "is_superuser", "is_staff")  # Фильтры
    search_fields = ("email", "username")  # Поля для поиска
    ordering = ("email",)  # Сортировка по email
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_active", "is_staff"),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
