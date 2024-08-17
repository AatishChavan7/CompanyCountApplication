from django import forms
from .models import CompanyFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CompanyFile
        fields = ['file']