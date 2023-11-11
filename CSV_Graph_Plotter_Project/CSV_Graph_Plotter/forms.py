from django import forms
from .models import UploadedCSV

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCSV
        fields = ['title', 'csv_file', 'x_column', 'y_column']
