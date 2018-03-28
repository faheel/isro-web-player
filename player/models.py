from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='uploads')
    
    CLOUD_COVER = 'cloud_cover'
    IMAGE_TYPE_CHOICES = (
        (CLOUD_COVER, 'Cloud cover'),
    )
    image_type = models.CharField(max_length=64, choices=IMAGE_TYPE_CHOICES, default=CLOUD_COVER)
    
    date = models.DateField()
    time = models.TimeField()
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ('date', 'time')
