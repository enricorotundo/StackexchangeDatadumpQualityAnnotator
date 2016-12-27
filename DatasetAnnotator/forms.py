from django import forms

from .models import *

class PostForm(forms.ModelForm):
    name = forms.CharField()
    quality = forms.IntegerField(label='quality')

    def ciao(self):
        print "ciao"

    class Meta:
        model = Post
        fields = ('annotatedquality',)