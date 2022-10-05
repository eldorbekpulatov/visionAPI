from django import forms

class UploadFileForm(forms.Form):
    file_name = forms.FilePathField(path='faces/', match="(?i)\.(jpg|png)$", required=True)
    