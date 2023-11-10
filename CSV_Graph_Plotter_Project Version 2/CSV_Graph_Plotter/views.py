# from django.shortcuts import render, HttpResponse

# # Create your views here.
# def index(request):
#     context={
#         'variable1' : 'I am Shrayansh',
#     }
#     return render(request, 'index.html', context)
#     # return HttpResponse("This is Home page")

# def about(request):
#     return HttpResponse("This is about page")

# def services(request):
#     return HttpResponse("This is services page")

# def contact(request):
#     return HttpResponse("This is contact page")

from django.shortcuts import render, redirect, HttpResponse
from .forms import CSVUploadForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def index(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_csv = form.save()
            # Process the CSV file and generate a plot here
            # Example: Generate a simple line plot
            title = uploaded_csv.title
            data = pd.read_csv(uploaded_csv.csv_file)
            plt.plot(data['X'], data['Y'])
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return render(request, 'plot.html', {'title': title,'chart': chart})
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})


def about(request):
    return HttpResponse("This is about page")

def services(request):
    return HttpResponse("This is services page")

def contact(request):
    return HttpResponse("This is contact page")
