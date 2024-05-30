import requests
from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView
from apps.core.utils.web_utils import WebUtils
from munchkin.components.base import POSTGREST_BASE_URL


class PostgrestAPIView(APIView):

    def forward_request(self, request: HttpRequest, method: str, path: str) -> HttpResponse:
        # Prepare the URL for the forwarded request
        url = POSTGREST_BASE_URL + '/' + path

        # Prepare the headers for the forwarded request
        headers = {
            'Content-Type': request.META.get('CONTENT_TYPE'),
            'accept': 'application/json',
        }

        if 'HTTP_RANGE_UNIT' in request.META:
            headers['Range-Unit'] = request.META['HTTP_RANGE_UNIT']

        if 'HTTP_PREFER' in request.META:
            headers['Prefer'] = request.META['HTTP_PREFER']
        # Send the forwarded request and get the response
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=request.GET,
            data=request.body,
        )

        # Return the response
        return WebUtils.response_success(response_data=response.json(), meta=dict(response.headers))

    def get(self, request: HttpRequest, path: str) -> HttpResponse:
        return self.forward_request(request, 'GET', path)

    def post(self, request: HttpRequest, path: str) -> HttpResponse:
        return self.forward_request(request, 'POST', path)

    def put(self, request: HttpRequest, path: str) -> HttpResponse:
        return self.forward_request(request, 'PUT', path)

    def delete(self, request: HttpRequest, path: str) -> HttpResponse:
        return self.forward_request(request, 'DELETE', path)
