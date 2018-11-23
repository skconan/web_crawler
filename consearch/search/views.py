from django.shortcuts import render
from .forms import Concert
from .my_elasticsearch import ElasticSearch

es = ElasticSearch()

# Create your views here.
def search(req): 
    form = Concert(req.POST)
    if form.is_valid():
        name = form.cleaned_data['concert_name']
        city = form.cleaned_data['city']
        date = form.cleaned_data['date']
        artist = form.cleaned_data['artist']
        keyword = form.cleaned_data['keyword']
        table_header, table_data = es.search(name,city)
        field = {
            'header':table_header,
            'rows':table_data
        }
        form = Concert()
    context = {'form':form,'field':field}
    template = 'search.html'
    return render(req, template, context)

