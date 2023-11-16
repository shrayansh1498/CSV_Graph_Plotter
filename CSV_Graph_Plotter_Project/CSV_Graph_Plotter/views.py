# from django.shortcuts import render, HttpResponse

# # Create your views here.
# def index(request):
#     context={
#         'variable1' : 'I am Shrayansh',
#     }
#     return render(request, 'index.html', context)
#     # return HttpResponse("This is Home page")

from django.shortcuts import render, redirect, HttpResponse
from .forms import CSVUploadForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib import messages #for error display

def index(request):
    error_message = None  # Initialize error_message as None
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_csv = form.save()
            # Process the CSV file and generate a plot here
            # Example: Generate a simple line plot
            title = uploaded_csv.title

            try:
                data = pd.read_csv(uploaded_csv.csv_file)

            # if the CSV has no columns i.e. no data, then it will run
            except pd.errors.EmptyDataError:
                error_message = "The uploaded CSV file has no data. Please upload a valid CSV file."
                return render(request, 'error.html', {'error_message': error_message})


            # Allow users to specify X and Y column names
            # x_column = request.POST.get('x_column')
            # y_column = request.POST.get('y_column')
            x_column = uploaded_csv.x_column
            y_column = uploaded_csv.y_column

            # Check if x and y columns exist in the data
            if x_column not in data.columns:
                error_message = "The specified X column does not exist in the CSV file. Please enter correct column name."
                return render(request, 'error.html', {'error_message': error_message})
            
            elif y_column not in data.columns:
                error_message = "The specified Y column does not exist in the CSV file. Please enter correct column name."
                return render(request, 'error.html', {'error_message': error_message})
            
            else:
                plot_data = data.dropna(subset=[x_column, y_column])
                plt.plot(plot_data[x_column], plot_data[y_column])
                plt.xlabel(x_column)
                plt.ylabel(y_column)

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
                return render(request, 'plot.html', {'title': title,'chart': chart})
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form, 'error_message' : error_message})


def about(request):
    return HttpResponse("This is about page")

def services(request):
    return HttpResponse("This is services page")

def contact(request):
    return HttpResponse("This is contact page")
