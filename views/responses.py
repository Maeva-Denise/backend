from flask import Response

from .utils import parse_response_data

class JSONResponse(Response):
    def __init__(self, response=None, status = None, headers = None, mimetype = None, content_type = "application/json", direct_passthrough = False, data=None) -> None:
        if data is not None:
            response = parse_response_data(data)

        super().__init__(response, status, headers, mimetype, content_type, direct_passthrough)

instance_not_found_response = Response("<h1>Instance not found</h1>", status=404)