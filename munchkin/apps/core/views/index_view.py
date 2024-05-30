from django.shortcuts import render


def index(request):
    data = {
    }
    response = render(request, "index.html", data)
    return response
