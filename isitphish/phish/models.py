from django.contrib import admin
from django.db import models

class URLFeatures(models.Model):
    URL = models.CharField(max_length=2000)
    def __str__(self):
        return self.URL

admin.site.register(URLFeatures)