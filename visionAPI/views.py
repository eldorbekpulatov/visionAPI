from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import UploadFileForm
from .markup import *
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def faceExtract(request):
    if request.method=="POST":
        if 'file_name' in request.POST:  
            file_name=request.POST['file_name']
        else:
            return render(request, '404.html')
    
        # here we call the api
        image, faces = getCoordinatesForFaces(file_name)
        if request.POST['api_choice'] == 'coordinatesOnly':
            return HttpResponse(faces, content_type='application/json')
        elif request.POST['api_choice'] == 'markedImageToo':
            return HttpResponse(faces, content_type='application/json')
        
    else:
        return render(request, 'faceExtract.html', {'form': UploadFileForm()})


def faceLandmark(request):
    if request.method=="POST":
        if 'file_name' in request.POST:  
            file_name=request.POST['file_name']
        else:
            return render(request, '404.html')
    
        # here we call the api
        image, faces = getCoordinatesForFaces(file_name)
        if request.POST['api_choice'] == 'coordinatesOnly':
            for k,v in faces.items(): 
                faces[k] = convertVectorToDict(v)
            return HttpResponse(json.dumps(faces, cls=NpEncoder), 
                                content_type='application/json')
        
        elif request.POST['api_choice'] == 'markedImageOnly':
            for k,v in faces.items():
                image = visualize_facial_landmarks(image, v)
                faces[k] = convertVectorToDict(v)
            cv2.imwrite("./media/output.png", image)

            return HttpResponse("/media/output.png", content_type='text/plain')
        
    else:
        return render(request, 'faceLandmark.html', {'form': UploadFileForm()})