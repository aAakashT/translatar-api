from django.db import models
from django.contrib.auth.models import User

class TranslationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    source_text = models.TextField(null=True, blank=True)
    source_language = models.CharField(max_length=10, null=True, blank=True)
    target_language = models.CharField(max_length=10, null=True, blank=True)
    translated_text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.source_text[:50]}"

    class Meta:
        ordering = ['-timestamp']