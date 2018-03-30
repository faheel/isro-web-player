import os
import uuid

from django.db import models


class Image(models.Model):
    def get_file_path(self, instance, filename):
        self.name = filename
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('uploads', filename)
    
    image = models.ImageField(upload_to=get_file_path)
    
    CLOUD_COVER = 'cloud_cover'
    IMAGE_TYPE_CHOICES = (
        (CLOUD_COVER, 'Cloud cover'),
    )
    
    image_type = models.CharField(max_length=64, choices=IMAGE_TYPE_CHOICES, default=CLOUD_COVER)
    
    name = models.CharField(max_length=64)
    
    date_time = models.DateTimeField()
    
    class Meta:
        ordering = ['date_time']
        unique_together = ('image_type', 'date_time')
