from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['tipo','mensaje','nombre','email']
        widgets = {
            'tipo': forms.Select(attrs={'class':'form-select'}),
            'mensaje': forms.Textarea(attrs={'class':'form-control','rows':4, 'placeholder':'Describe tu idea, bug o sugerencia...'}),
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Opcional si no tienes cuenta'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Opcional para respuesta'}),
        }
