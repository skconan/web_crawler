from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class Concert(forms.Form):
    IS_RANKING = (
        (0, ("Unranking")),
        (1, ("Ranking"))
    )
    concert_name = forms.CharField(required=False,max_length=100)
    city = forms.CharField(required=False,max_length=100)
    start_date = forms.DateField(
        widget=DatePickerInput(format='%Y-%m-%d'),required=False
    )
    end_date = forms.DateField(
        widget=DatePickerInput(format='%Y-%m-%d'),required=False
    )
    # artist = forms.CharField(required=False,max_length=100)
    # keyword = forms.CharField(required=False,max_length=100)
    # ranking = forms.ChoiceField(choices=IS_RANKING,initial=0,required=False)