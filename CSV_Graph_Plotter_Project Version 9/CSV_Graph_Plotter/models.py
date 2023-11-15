from django.db import models

# Create your models here.

class UploadedCSV(models.Model):
    title = models.CharField(max_length=255)
    csv_file = models.FileField(upload_to='')
    x_column = models.CharField(max_length=255, default='X')
    y_column = models.CharField(max_length=255, default='Y')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
