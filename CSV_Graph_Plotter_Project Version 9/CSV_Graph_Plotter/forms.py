from django import forms
from .models import UploadedCSV

def validate_csv_extension(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError('Only CSV files are allowed.')

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCSV
        fields = ['title', 'csv_file', 'x_column', 'y_column']
        
    csv_file = forms.FileField(validators=[validate_csv_extension])