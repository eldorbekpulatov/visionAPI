import time 
import requests

# Variables
KEY = 'ce57989e94e74a64ba1e517f58ab2671'


class AzureRequest:
    def __init__(self, credentials, region='southcentralus'):
        self.credentials = credentials
        self.region = region

    
    def get_response(self, image_Path_or_File):
        """Returns the API result from Microsoft Azure.
        
        Params: 
            imagePath : string containing a path to local file or a link 
        """

        # Computer Vision parameters
        params = {
            # Request parameters
            'language': 'en',
            'detectOrientation ': 'true',
        }

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.credentials,
        }

        try:
            try:
                # Load raw image file into memory
                with open(image_Path_or_File, 'rb' ) as f:
                    data = f.read()
            except:
                data = image_Path_or_File
            
            if data!=None:
                headers['Content-Type'] = 'application/octet-stream'
                json = None
        except:
            # URL direction to image
            json = { 'url': image_Path_or_File } 
            headers['Content-Type'] = 'application/json'
            data = None

        result = processRequest( json, data, headers, params, self.region )

        return result


def processRequest( json, data, headers, params, region ):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None
    _maxNumRetries = 10
    _url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/ocr?'.format(region)

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        
        if response.status_code == 429: 

            print( "Message: %s" % ( response.json() ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
            # this was to print the response link for text scan
            # print response.headers['Operation-Location']
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )

        break
        
    return result
