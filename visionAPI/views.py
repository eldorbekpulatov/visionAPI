from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import UploadFileForm
from .settings import BASE_DIR


import json
from .google import GoogleRequest
from .azure import AzureRequest
from .models import Architect, Sample, Phrase

# to serialize google's response 
from google.protobuf.json_format import MessageToJson


def rawResponse(request):
    # init apis
    gkey=BASE_DIR+'/googlevision.json'
    akey='ce57989e94e74a64ba1e517f58ab2671'
    grequest=GoogleRequest(gkey)
    arequest = AzureRequest(akey)


    if request.is_ajax() and request.method=="POST":
        if 'file_name' in request.POST:  
            file_name=request.POST['file_name']
        else:
            file_name=None
    
        # here we call the api    
        if request.POST['api_choice'] == 'azure':
            api_result=json.dumps(arequest.get_response(file_name))
        elif request.POST['api_choice'] == 'google':
            api_result=MessageToJson(grequest.get_response(file_name))
        
        return HttpResponse(api_result, content_type='application/json')
    else:
        form = UploadFileForm()
        return render(request, 'rawResponse.html', {'form': form})



def addProfile(request):
    if request.is_ajax() and request.method=="POST":
        # collect attr
        name = request.POST['name']
        path = request.POST['path']
        sampleSet = getSampleSet(request.POST['sampleSet'].split(","))
        phrases = request.POST['phrases'].split(",")
        # save the profile
        saveProfileToDB(name, path, phrases, sampleSet)
        # output JSON
        outputJSON(name, path, phrases, sampleSet)

        return HttpResponse('Successfully Added!')
    else:
        return render(request, 'addProfile.html')


def profileDirectory(request):
    architects= Architect.objects.all()
    context={"architects" : architects}
    return render(request, 'profileDirectory.html', context)





####################
# Helper functions #
####################
def getSampleSet(array):
    sampleSet=[]
    for eachSample in array:
        sample={}
        s_str = eachSample.split(";")
        s_id = int(s_str[0])
        s_page = int(s_str[1])
        sample["id"]=s_id
        sample["page"]=s_page
        sampleSet.append(sample)
    return sampleSet

def outputJSON(name, path, phrases, sampleSet):
    profile={
        "name"  : name,
        "path"  : path,
        "phrases"   : phrases,
        "sampleSet" : sampleSet
    }
    with open("C:/Users/gamyte/Desktop/profiles/"+name+".json", "w") as outfile:
        outfile.write(json.dumps(profile))

def saveProfileToDB(name, path, phrases, sampleSet):
    """Saves the profile to DataBase"""
    # init architect
    architect = Architect()
    architect.name = name
    architect.path = path
    architect.save()
    # init samples
    for sample in sampleSet:
        sam=Sample()
        sam.sampleID=sample["id"]
        sam.page=sample["page"]
        sam.architect=architect
        sam.save()
    # init phrases
    for phrase in phrases:
        phr=Phrase()
        phr.phrase=phrase
        phr.architect=architect
        phr.save()