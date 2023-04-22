# Aqui puedo crear formularios a partir de los modelos
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        # Aqui va el modelo en el que se basa el form
        model = Task
        # Los campos que se utilizaran para formar el formulario
        fields = ['title', 'description', 'important']
        # Con los widgets puedo añadir clases para cambiar el estilo a html que viene de django
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'})
        }