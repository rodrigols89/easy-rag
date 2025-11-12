from django import forms

from .models import File, Folder


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name"]  # campo que o usuário vai preencher


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]
