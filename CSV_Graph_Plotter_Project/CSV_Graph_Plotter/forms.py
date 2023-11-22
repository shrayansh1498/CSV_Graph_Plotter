from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UploadedCSV

def validate_csv_extension(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError('Only CSV files are allowed.')

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCSV
        fields = ['title', 'csv_file', 'x_column', 'y_column', 'y1_column', 'y2_column', 'y3_column']
        
    csv_file = forms.FileField(validators=[validate_csv_extension])

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']