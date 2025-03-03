from django import forms
from .models import UseCaseDiagram, ClassDiagram

class UseCaseDiagramForm(forms.ModelForm):
    class Meta:
        model = UseCaseDiagram
        fields = ['name', 'description', 'file']

class ClassDiagramForm(forms.ModelForm):
    class Meta:
        model = ClassDiagram
        fields = ['name', 'description', 'file']