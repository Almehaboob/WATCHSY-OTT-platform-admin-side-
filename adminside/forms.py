from django import forms
from apiside.models import Movie ,Plan


class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['title','thumbnail','video','description','rating']
        
        
        
        
class PlanForm(forms.ModelForm):
    class Meta:
        model=Plan
        fields=['name','thumbnail','price','duration']
        
