from django import forms
from .models import Comments

# Для таблиці Products forms.py е прописується оскільки можливість додавання товару через сайт на процесі розробки не запланована


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Коментар' ,
                'rows': '3' ,                   # показує 3 рядки висоти при створенні коментаря
            })
        }