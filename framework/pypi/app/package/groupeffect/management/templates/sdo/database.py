from django.db import models

# Create your models here.


class GroupeffectNamespace(models.Model):
    namespace = models.CharField(max_length=200, blank=True, null=True)
    uri = models.URLField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
