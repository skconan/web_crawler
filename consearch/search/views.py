from django.shortcuts import render
from .forms import Concert
from .my_elasticsearch import ElasticSearch

es = ElasticSearch()

# Create your views here.


def search(req):
    form = Concert(req.POST)
    context = {'form': form}
    if form.is_valid():
        data = {
            'name':None,
            'city':None,
            'start_date':None,
            'end_date':None,
            'artist':None,
            'keyword':None,
        }
        data['concert_name'] = form.cleaned_data['concert_name']
        data['city'] = form.cleaned_data['city']
        data['start_date'] = form.cleaned_data['start_date']
        data['end_date'] = form.cleaned_data['end_date']
        # data['artist'] = form.cleaned_data['artist']
        # data['keyword'] = form.cleaned_data['keyword']
        # is_ranking = form.cleaned_data['ranking']
        # is_ranking = is_ranking == '1'
        key = []
        value = []     
        table_header = []
        table_data = []   
        for k in data.keys():
            if not k.find('date') >= 0 and data[k] != None and data[k] != "":
                key.append(k)
                value.append(data[k])
        if data['start_date'] != None and data['end_date'] != None:
            table_header, table_data = es.search(key, value,data['start_date'],data['end_date'] )
        elif data['start_date'] != None :
            table_header, table_data = es.search(key, value,data['start_date'] )
        elif data['end_date'] != None:
            table_header, table_data = es.search(key, value,end_date=data['end_date'] )
        else:
            table_header, table_data = es.search(key, value )
        field = {
            'header': table_header,
            'rows': table_data
        }
        context = {'form': form, 'field': field}

        form = Concert()
    template = 'search.html'
    return render(req, template, context)
