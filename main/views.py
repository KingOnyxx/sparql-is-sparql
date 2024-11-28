from django.shortcuts import render
from rdflib import Graph, URIRef, Literal, Namespace

# Create your views here.

def home(request):
    return render(request, 'index.html')


def search(request):
    if request.method == "GET":
        # search = request.GET.get('search')
        # print(search)
        query = ""
    return True
    