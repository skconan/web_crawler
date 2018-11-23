from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class Concert(forms.Form):
    IS_RANKING = (
        (1, ("Unranking")),
        (2, ("Ranking"))
    )
    concert_name = forms.CharField(required=False,max_length=100)
    city = forms.CharField(required=False,max_length=100)
    date = forms.DateField(
        widget=DatePickerInput()
    )
    artist = forms.CharField(required=False,max_length=100)
    keyword = forms.CharField(required=False,max_length=100)
    ranking = forms.ChoiceField(choices=IS_RANKING,initial=1)