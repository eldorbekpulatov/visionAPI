from django import forms

class UploadFileForm(forms.Form):
    file_name = forms.FilePathField(path='C:/Users/gamyte/Desktop/samples/', match=".*\.png$", recursive=True)
    