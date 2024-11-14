from django.contrib import admin

from .models import User, AttendanceManagement


class UserAdmin(admin.ModelAdmin):
    # リストでの表示フィールド指定
    list_display = ["username", "full_name", "email", "is_active", "on_work", "last_login", "authority"]

    list_filter = ["username", "full_name", "contract_type", "authority", "date_joined"]

    search_fields = ["username", "full_name", "contract_type", "email", "phone"]

    fieldsets = [
        (None, {"fields": ["full_name"]}),
        ("詳細情報",{
                "fields": ["username",
                           "gender",
                           "birth",
                           "email",
                           "phone",
                           "introduction",
                           "on_work",
                           "contract_type",
                           "authority",
                           ]
                }
        ),
        ("管理情報", {
                "classes": ["collapse"],
                "fields": ["is_staff", "is_active", "is_superuser", "password"]
                }
        ),
        ("日付情報", {
                "classes": ["collapse"],
                "fields": ["date_joined", "last_login"]
                }
        ),
    ]

class AttendanceManagementAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "type", "time"]

admin.site.register(User, UserAdmin)
admin.site.register(AttendanceManagement, AttendanceManagementAdmin)