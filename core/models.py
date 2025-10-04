from django.db import models


class Recording(models.Model):
    device_id = models.CharField(max_length=128, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    audio_file = models.FileField(upload_to='recordings/')
    created_at = models.DateTimeField(auto_now_add=True)
    # simple analysis results stored as JSON (models.JSONField is DB-agnostic)
    analysis = models.JSONField(blank=True, null=True, default=dict)
    is_drone_suspicious = models.BooleanField(default=False)

    def __str__(self):
        return f"Recording {self.id} from {self.device_id or 'unknown'}"
