from django import forms
from dal import autocomplete
from imports.models import Pa


class PaForm(forms.Form):
    pa = forms.CharField(max_length=50)
    pa_selector = forms.ModelChoiceField(queryset=Pa.objects.all(), widget=autocomplete.ModelSelect2(url='pa-autocomplete'), type='visible')

    class Meta:
        model: Pa
        fields = ('__all__')
