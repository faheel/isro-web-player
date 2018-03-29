from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='uploads')
    
    CLOUD_COVER = 'cloud_cover'
    IMAGE_TYPE_CHOICES = (
        (CLOUD_COVER, 'Cloud cover'),
    )
    image_type = models.CharField(max_length=64, choices=IMAGE_TYPE_CHOICES, default=CLOUD_COVER)
    
    date_time = models.DateTimeField()
    
    class Meta:
        ordering = ['date_time']
        unique_together = ('image_type', 'date_time')
