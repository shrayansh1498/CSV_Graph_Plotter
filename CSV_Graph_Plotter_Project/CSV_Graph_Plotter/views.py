# from django.shortcuts import render, HttpResponse

# # Create your views here.
# def index(request):
#     context={
#         'variable1' : 'I am Shrayansh',
#     }
#     return render(request, 'index.html', context)
#     # return HttpResponse("This is Home page")

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CSVUploadForm, CreateUserForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib import messages #for error display
import numpy as np

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
            y1_column = uploaded_csv.y1_column
            y2_column = uploaded_csv.y2_column
            y3_column = uploaded_csv.y3_column

            # Check if x and y columns exist in the data
            if x_column not in data.columns:
                error_message = "The specified X column does not exist in the CSV file. Please enter correct column name."
                return render(request, 'error.html', {'error_message': error_message})
            
            if y_column not in data.columns:
                error_message = "The specified Y column does not exist in the CSV file. Please enter correct column name."
                return render(request, 'error.html', {'error_message': error_message})
            
            if y1_column:
                if y1_column not in data.columns:
                    error_message = "The specified X1 column does not exist in the CSV file. Please enter correct column name."
                    return render(request, 'error.html', {'error_message': error_message})

            if y2_column:
                if y2_column not in data.columns:
                    error_message = "The specified X2 column does not exist in the CSV file. Please enter correct column name."
                    return render(request, 'error.html', {'error_message': error_message})

            if y3_column:
                if y3_column not in data.columns:
                    error_message = "The specified X3 column does not exist in the CSV file. Please enter correct column name."
                    return render(request, 'error.html', {'error_message': error_message})
            
            
            #dropna is used to skip row in case any of the column contains null value
            plot_data = data.dropna(subset=[x_column, y_column])

            # Check if there are data points to plot
            if plot_data.empty:
                error_message = "No data points to plot."
                return render(request, 'error.html', {'error_message': error_message})

            # Line Graph
            plt.plot(plot_data[x_column], plot_data[y_column],  marker='o', linestyle='-', markersize=3)
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            if y1_column:
                plot_data1 = data.dropna(subset=[x_column, y1_column])
                plt.plot(plot_data1[x_column], plot_data1[y1_column],  marker='o', linestyle='-', markersize=3)
            if y2_column:
                plot_data2 = data.dropna(subset=[x_column, y2_column])
                plt.plot(plot_data2[x_column], plot_data2[y2_column],  marker='o', linestyle='-', markersize=3)
            if y3_column:
                plot_data3 = data.dropna(subset=[x_column, y3_column])
                plt.plot(plot_data3[x_column], plot_data3[y3_column],  marker='o', linestyle='-', markersize=3)
                

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            lineChart = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Bar Graph
            bar_width = 0.2  # Adjust the width of the bars
            
            plt.bar(plot_data[x_column], plot_data[y_column], width=bar_width, label=y_column)
            plt.xlabel(x_column)
            plt.ylabel(y_column)

            # if y1_column:
            #     plt.bar(plot_data[x_column], plot_data[y1_column])
            # if y2_column:
            #     plt.bar(plot_data[x_column], plot_data[y2_column])
            # if y3_column:
            #     plt.bar(plot_data[x_column], plot_data[y3_column])

            if y1_column:
                plt.bar(np.array(plot_data[x_column]) + bar_width, plot_data[y1_column], width=bar_width, label=y1_column)
            if y2_column:
                plt.bar(np.array(plot_data[x_column]) + 2*bar_width, plot_data[y2_column], width=bar_width, label=y2_column)
            if y3_column:
                plt.bar(np.array(plot_data[x_column]) + 3*bar_width, plot_data[y3_column], width=bar_width, label=y3_column)


            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            barChart = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Scatter Graph
            plt.scatter(plot_data[x_column], plot_data[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            scatterChart = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Histogram Graph for X axis
            r = 10
            if pd.api.types.is_numeric_dtype(plot_data[x_column]):
                r = np.arange(min(plot_data[x_column]), max(plot_data[x_column]) + 2)
            plt.hist(plot_data[x_column], bins=r, align='left')
            plt.xlabel(x_column)
            plt.ylabel("Frequency")

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            histogramChart1 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Histogram Graph for Y axis
            r = 10
            if pd.api.types.is_numeric_dtype(plot_data[y_column]):
                r = range(int(min(plot_data[y_column])), int(max(plot_data[y_column])) + 2)
            plt.hist(plot_data[y_column], bins=r, align='left')
            plt.xlabel(y_column)
            plt.ylabel("Frequency")

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            histogramChart2 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return render(request, 'plot.html', {'title': title,'lineChart': lineChart, 'barChart': barChart, 'scatterChart': scatterChart, 'histogramChart1': histogramChart1,'x_column': x_column, 'histogramChart2': histogramChart2, 'y_column': y_column})
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form, 'error_message' : error_message})


def about(request):
    return HttpResponse("This is about page")

def services(request):
    return HttpResponse("This is services page")

def contact(request):
    return HttpResponse("This is contact page")

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been successfully Created.')
            return redirect("/")
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})
