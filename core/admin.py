from django.contrib import admin
from .models import Recording


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'timestamp', 'created_at')
