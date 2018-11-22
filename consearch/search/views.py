from django.shortcuts import render

# Create your views here.
def search(req): 
    context = {}
    template = 'search.html'
    return render(req, template, context)