from msilib.schema import Feature
from pyexpat import features
from django.shortcuts import render
import mimetypes
#from sih.AutoFeatureSelection import FeatureSelection
from sih.AutoFeatureSelection import *
from django.core.files.storage import FileSystemStorage
#import AutoFeatureSelection
from sih.models import File_Data


from sih.Cleaner import *
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import os
#from somewhere import handle_uploaded_file


from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
from django.http import HttpResponse
import pandas as pd


#def index(request):
 #   return HttpResponse("Hello, SIH")
def index(request):

    return render(request,'index.html')

def Save_File(request):
    if request.method=='POST':
        a=request.FILES['file']
        print(a)
        df = pd.read_csv(a)
        print("row data :", df.head())
        print("row data shape :", df.shape)
        target = "Loan_Status"
        date = "date"
        frequency_sampling_type = None
        X, Y = AutoFeatureSelection.FeatureSelection(df, target)  #
        # res=dataCleaner(df,features,target,DictionaryClass=None)
        print("final df Shape :", X.shape)

        print("Finale dataframe :", X.head())

        my_data=File_Data.objects.create(files=a)
        my_data.save()
        return HttpResponse("Form Submitted")

def nlp(request):
    return render(request,'nlp.html')

def nlpfile(request):
    if request.method=='POST':
        a=request.FILES['nlp']
        print(a)
        df = pd.read_csv(a)\

        print("row data :", df.head())
        print("row data shape :", df.shape)
        target = "Loan_Status"
        date = "date"
        frequency_sampling_type = None
        X, Y = AutoFeatureSelection.FeatureSelection(df, target)  #
        # res=dataCleaner(df,features,target,DictionaryClass=None)
        print("final df Shape :", X.shape)

        print("Finale dataframe :", X.head())

        my_data=File_Data.objects.create(files=a)
        my_data.save()

        print(a.name)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/media/' + a.name
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % a.name
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'index.html')


#    return HttpResponse("Form Submitted")

def classi(request):
    return render(request,'classi.html')


def classifile(request):
    if request.method=='POST':
        a=request.FILES['classi']
        print(a)
        df = pd.read_csv(a)\

        print("row data :", df.head())
        print("row data shape :", df.shape)
        target = "Loan_Status"
        date = "date"
        frequency_sampling_type = None
        X, Y = AutoFeatureSelection.FeatureSelection(df, target)  #
        # res=dataCleaner(df,features,target,DictionaryClass=None)
        print("final df Shape :", X.shape)

        print("Finale dataframe :", X.head())

        my_data=File_Data.objects.create(files=a)
        my_data.save()

        print(a.name)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/media/' + a.name
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % a.name
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'index.html')


#    return HttpResponse("Form Submitted")

def ts(request):
    return render(request,'ts.html')


def tsfile(request):
    if request.method=='POST':
        a=request.FILES['ts']
        print(a)
        df = pd.read_csv(a)\

        print("row data :", df.head())
        print("row data shape :", df.shape)
        target = "Loan_Status"
        date = "date"
        frequency_sampling_type = None
        X, Y = AutoFeatureSelection.FeatureSelection(df, target)  #
        # res=dataCleaner(df,features,target,DictionaryClass=None)
        print("final df Shape :", X.shape)

        print("Finale dataframe :", X.head())

        my_data=File_Data.objects.create(files=a)
        my_data.save()
        print(a.name)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/media/' + a.name
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % a.name
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'index.html')


#    return HttpResponse("Form Submitted")

def vid(request):
    return render(request,'vid.html')


def vidfile(request):
    if request.method=='POST':
        a=request.FILES['vid']
        print(a)
        df = pd.read_csv(a)\

        print("row data :", df.head())
        print("row data shape :", df.shape)
        target = "Loan_Status"
        date = "date"
        frequency_sampling_type = None
        X, Y = AutoFeatureSelection.FeatureSelection(df, target)  #
        # res=dataCleaner(df,features,target,DictionaryClass=None)
        print("final df Shape :", X.shape)

        print("Finale dataframe :", X.head())

        my_data=File_Data.objects.create(files=a)
        my_data.save()

        print(a.name)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/media/' + a.name
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type,_ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % a.name
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'index.html')
#    return HttpResponse("Form Submitted")
