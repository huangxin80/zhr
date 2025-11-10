from django.contrib import admin
from .models import Job, Application

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'salary', 'salary_type', 'publisher', 'status', 'created_at')
    list_filter = ('category', 'status', 'salary_type', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'applicant__username', 'message')
    readonly_fields = ('created_at', 'updated_at')
