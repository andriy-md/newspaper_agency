from django.contrib import admin

from newspaper.models import Redactor, Topic, Newspaper


@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + (
        "username", "first_name", "last_name", "email", "years_of_experience",
    )
    fieldsets = [
        (
            "Main Information",
            {
                "fields": ["username", "first_name", "last_name", "email", "years_of_experience"]
            }
        ),
        (
            "Advanced",
            {
                "fields": [
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "last_login",
                    "date_joined",
                    "groups",
                    "user_permissions"
                ]
            }
        )
    ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ["title", "topic"]
