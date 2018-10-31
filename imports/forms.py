from django import forms

from imports.models import ImportOptimum, Pa


class ImportFileForm(forms.Form):
    csv_file = forms.FileField()

    class Meta:
        model = ImportOptimum
