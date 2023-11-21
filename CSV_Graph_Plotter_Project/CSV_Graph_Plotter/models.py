from django.db import models

# Create your models here.

class UploadedCSV(models.Model):
    title = models.CharField(max_length=255)
    csv_file = models.FileField(upload_to='')
    x_column = models.CharField(max_length=255, default='X')
    y_column = models.CharField(max_length=255, default='Y')
    x1_column = models.CharField(max_length=255, null=True, blank=True)
    x2_column = models.CharField(max_length=255, null=True, blank=True)
    x3_column = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
