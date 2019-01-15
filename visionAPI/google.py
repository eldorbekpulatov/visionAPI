import io
import os
import json
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.cloud.vision_v1 import ImageAnnotatorClient

# export GOOGLE_APPLICATION_CREDENTIALS='/Users/eldorbekpualtov/Desktop/google/visionAPI/visionAPI/googlevision.json'

class GoogleRequest:
    def __init__(self, credentials):
        self.credentials = credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']=self.credentials
    
    def get_response(self, image_Path_or_File):
        """Returns document bounds given an image."""

        client = ImageAnnotatorClient()

        try:
            with io.open(image_Path_or_File, 'rb') as image_file:
                content = image_file.read()
        except:
            content = image_Path_or_File
        
        image = types.Image(content=content)

        response = client.document_text_detection(image=image)
        original = response.full_text_annotation
 
        return original

