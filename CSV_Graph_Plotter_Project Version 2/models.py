from django.db import models

# Create your models here.

class UploadedCSV(models.Model):
    title = models.CharField(max_length=255)
    csv_file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
