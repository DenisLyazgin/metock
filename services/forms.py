from django import forms
from .models import Video


class VideoDescriptionForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['description']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['description', 'video_file']
