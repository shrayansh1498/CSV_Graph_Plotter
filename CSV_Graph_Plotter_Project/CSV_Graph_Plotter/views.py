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

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages #for error display
import numpy as np

@login_required(login_url='/login')
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
                    error_message = "The specified Y1 column does not exist in the CSV file. Please enter correct column name."
                    return render(request, 'error.html', {'error_message': error_message})

            if y2_column:
                if y2_column not in data.columns:
                    error_message = "The specified Y2 column does not exist in the CSV file. Please enter correct column name."
                    return render(request, 'error.html', {'error_message': error_message})

            if y3_column:
                if y3_column not in data.columns:
                    error_message = "The specified Y3 column does not exist in the CSV file. Please enter correct column name."
                    return render(request, 'error.html', {'error_message': error_message})
            
            
            #dropna is used to skip row in case any of the column contains null value
            plot_data = data.dropna(subset=[x_column, y_column])

            # Check if there are data points to plot
            if plot_data.empty:
                error_message = "No data points to plot."
                return render(request, 'error.html', {'error_message': error_message})

            # Line Graph
            plt.figure(figsize=(15, 10))
            plt.plot(plot_data[x_column], plot_data[y_column], label=y_column, marker='o', linestyle='-', markersize=3)
            plt.legend()
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            if y1_column:
                plot_data1 = data.dropna(subset=[x_column, y1_column])
                plt.plot(plot_data1[x_column], plot_data1[y1_column], label=y1_column, marker='o', linestyle='-', markersize=3)
                plt.legend()
            if y2_column:
                plot_data2 = data.dropna(subset=[x_column, y2_column])
                plt.plot(plot_data2[x_column], plot_data2[y2_column], label=y2_column, marker='o', linestyle='-', markersize=3)
                plt.legend()
            if y3_column:
                plot_data3 = data.dropna(subset=[x_column, y3_column])
                plt.plot(plot_data3[x_column], plot_data3[y3_column], label=y3_column, marker='o', linestyle='-', markersize=3)
                plt.legend()
                

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            lineChart = base64.b64encode(buffer.getvalue()).decode('utf-8')


            # Bar Graph
            bar_width = 0.2  # Adjust the width of the bars
            plt.figure(figsize=(15, 10))
            plt.bar(plot_data[x_column], plot_data[y_column], width=bar_width, label=y_column)
            plt.legend()
            plt.xlabel(x_column)
            plt.ylabel(y_column)

            # if y1_column:
            #     plt.bar(plot_data[x_column], plot_data[y1_column])
            # if y2_column:
            #     plt.bar(plot_data[x_column], plot_data[y2_column])
            # if y3_column:
            #     plt.bar(plot_data[x_column], plot_data[y3_column])
            n=1

            if y1_column:
                # if type(y1_column[0]) == str:
                #     y1_column = np.arange(len(y1_column))
                plt.bar(np.array(plot_data1[x_column])+ n*bar_width , plot_data1[y1_column], width=bar_width, label=y1_column)
                plt.legend()
                n+=1
            if y2_column:
                plt.bar(np.array(plot_data2[x_column])+ n*bar_width , plot_data2[y2_column], width=bar_width, label=y2_column)
                plt.legend()
                n+=1
            if y3_column:
                plt.bar(np.array(plot_data3[x_column])+ n*bar_width , plot_data3[y3_column], width=bar_width, label=y3_column)
                plt.legend()


            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            barChart = base64.b64encode(buffer.getvalue()).decode('utf-8')


            # Scatter Graph
            plt.figure(figsize=(15, 10))
            plt.scatter(plot_data[x_column], plot_data[y_column], label=y_column)
            plt.legend()
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            

            if y1_column:
                plt.scatter(np.array(plot_data1[x_column]), plot_data1[y1_column], label=y1_column)
                plt.legend()
            if y2_column:
                plt.scatter(np.array(plot_data2[x_column]), plot_data2[y2_column], label=y2_column)
                plt.legend()
            if y3_column:
                plt.scatter(np.array(plot_data3[x_column]), plot_data3[y3_column], label=y3_column)
                plt.legend()

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            scatterChart = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Histogram Graph for X axis
            x_column_name = uploaded_csv.x_column
            x_values = plot_data[x_column_name].dropna()    
            plt.figure(figsize=(15, 10))
            hist, bin_edges, _ = plt.hist(x_values, bins=np.unique(x_values), align='mid', ec='black')
            plt.xlabel(x_column)
            plt.ylabel("Frequency")
            plt.xticks(bin_edges)

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            histogramChart1 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Histogram Graph for Y axis

            y_column_name = uploaded_csv.y_column
            y_values = plot_data[y_column_name].dropna()    
            plt.figure(figsize=(15, 10))
            hist, bin_edges, _ = plt.hist(y_values, bins=np.unique(y_values), align='mid', ec='black')
            plt.xlabel(y_column)
            plt.ylabel("Frequency")
            plt.xticks(bin_edges)

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            print("running")
            histogramChart2 = base64.b64encode(buffer.getvalue()).decode('utf-8')


            # Histogram Graph for Y1-column
            if y1_column and not plot_data1.empty:  # Check if y1_column is not blank and plot_data1 is not empty

                y1_column_name = uploaded_csv.y1_column
                y1_values = plot_data[y1_column_name].dropna()    
                plt.figure(figsize=(15, 10))
                hist, bin_edges, _ = plt.hist(y1_values, bins=np.unique(y1_values), align='mid', ec='black')
                plt.xlabel(y1_column)
                plt.ylabel("Frequency")
                plt.xticks(bin_edges)

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                histogramChart3 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            else:
                histogramChart3 = None  # Set to None if no histogram is plotted

            # Histogram Graph for Y2-column
            if y2_column and not plot_data2.empty:  # Check if y1_column is not blank and plot_data1 is not empty
                y2_column_name = uploaded_csv.y2_column
                y2_values = plot_data[y2_column_name].dropna()    
                plt.figure(figsize=(15, 10))
                hist, bin_edges, _ = plt.hist(y2_values, bins=np.unique(y2_values), align='mid', ec='black')
                plt.xlabel(y2_column)
                plt.ylabel("Frequency")
                plt.xticks(bin_edges)

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                histogramChart4 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            else:
                histogramChart4 = None  # Set to None if no histogram is plotted

            # Histogram Graph for Y3-column
            if y3_column and not plot_data3.empty:  # Check if y1_column is not blank and plot_data1 is not empty
                y3_column_name = uploaded_csv.y3_column
                y3_values = plot_data[y3_column_name].dropna()    
                plt.figure(figsize=(15, 10))
                hist, bin_edges, _ = plt.hist(y3_values, bins=np.unique(y3_values), align='mid', ec='black')
                plt.xlabel(y3_column)
                plt.ylabel("Frequency")
                plt.xticks(bin_edges)

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                histogramChart5 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            else:
                histogramChart5 = None  # Set to None if no histogram is plotted


            return render(request, 'plot.html', {'title': title,'lineChart': lineChart, 'barChart': barChart, 'scatterChart': scatterChart, 'histogramChart1': histogramChart1,'x_column': x_column, 'histogramChart2': histogramChart2, 'y_column': y_column, 'histogramChart3': histogramChart3, 'y1_column': y1_column, 'histogramChart4': histogramChart4, 'y2_column': y2_column, 'histogramChart5': histogramChart5, 'y3_column': y3_column})

    else:
        form = CSVUploadForm()
    return render(request, 'index.html', {'form': form, 'error_message' : error_message})


# def about(request):
#     return HttpResponse("This is about page")

# def services(request):
#     return HttpResponse("This is services page")

# def contact(request):
#     return HttpResponse("This is contact page")

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been successfully Created.')
            return redirect('/login')
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')         #if login successful, redirect to home page
        else:
            messages.info(request, "Username or Password is incorrect")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('/login')




def home(request):
    error_message = None  # Initialize error_message as None
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('/login')

    else:
        form = CSVUploadForm()
    return render(request, 'index.html', {'form': form, 'error_message' : error_message})
