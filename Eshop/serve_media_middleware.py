import os
import logging
from django.http import HttpResponse, HttpResponseNotFound
from mimetypes import guess_type
from django.conf import settings

logger = logging.getLogger(__name__)

class ServeMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(settings.MEDIA_URL):
            media_path = request.path.replace(settings.MEDIA_URL, "", 1)
            file_path = os.path.join(settings.MEDIA_ROOT, media_path)
            logger.debug(f"Attempting to serve media file at: {file_path}")
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    mime_type, _ = guess_type(file_path)
                    response = HttpResponse(f.read(), content_type=mime_type)
                    response["Content-Disposition"] = f"inline; filename={os.path.basename(file_path)}"
                    return response
            logger.warning(f"File not found: {file_path}")
            return HttpResponseNotFound("File not found")
        return self.get_response(request)
