import json

from models.base_model import AbstractBaseModel

def parse_request_data(request):
    data = request.data.decode()

    return json.loads(data)

def parse_response_data(data):
    """
    Convert model instance to appropriate data type for the response
    """
    dictionary = None

    if isinstance(data, AbstractBaseModel):
        
        try:
            dictionary = data.toJSON()
        except AttributeError:
            dictionary = data
            
    elif isinstance(data, dict):
        dictionary = data
    else:
        dictionary = data

    return json.dumps(dictionary)