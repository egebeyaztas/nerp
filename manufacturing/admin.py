from django.contrib import admin
from .models import JobOrder, JobOrderFile, TaskFlow, Task


class JobOrderFileInline(admin.TabularInline):
    model = JobOrderFile


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        JobOrderFileInline,
    ]

admin.site.register(JobOrder, FeedAdmin)
admin.site.register(TaskFlow)
admin.site.register(Task)
