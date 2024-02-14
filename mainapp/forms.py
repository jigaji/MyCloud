from django import forms 
from .models import Folder

class NewFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name',)