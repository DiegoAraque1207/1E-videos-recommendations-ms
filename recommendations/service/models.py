from django.db import models

# Create your models here.
class UserPreferences(models.Model):
    id_user = models.IntegerField(null=False)
    id_category = models.IntegerField(null=False)
    counter = models.IntegerField(default=1)
class VideoStatistics(models.Model):
    id_video = models.CharField(max_length=50, null=False)
    id_category = models.IntegerField(null=False)
    sumCalification = models.IntegerField(default=0)
    calicationsCount = models.IntegerField(default=1)
    num_views = models.IntegerField(default=1)