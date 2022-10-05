from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import UploadFileForm
import json


def faceExtract(request):
    d = {"hello": "there"}
    if request.method=="POST":
        if 'file_name' in request.POST:  
            file_name=request.POST['file_name']
        else:
            file_name=None
    
        # here we call the api    
        if request.POST['api_choice'] == 'azure':
            api_result=json.dumps(d)
        elif request.POST['api_choice'] == 'google':
            api_result=json.dumps(d)
        
        return HttpResponse(api_result, content_type='application/json')
    else:
        form = UploadFileForm()
        return render(request, 'faceExtract.html', {'form': form})


def faceLandmark(request):
    d = {"hello": "there"}
    if request.method=="POST":
        if 'file_name' in request.POST:  
            file_name=request.POST['file_name']
        else:
            file_name=None
    
        # here we call the api    
        if request.POST['api_choice'] == 'azure':
            api_result=json.dumps(d)
        elif request.POST['api_choice'] == 'google':
            api_result=json.dumps(d)
        
        return HttpResponse(api_result, content_type='application/json')
    else:
        form = UploadFileForm()
        return render(request, 'faceLandmark.html', {'form': form})