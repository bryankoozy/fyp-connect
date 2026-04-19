# dashboard/forms.py

from django import forms
from .models import FYPPost


class FYPPostForm(forms.ModelForm):
    class Meta:
        model = FYPPost
        fields = ['title', 'description', 'skills_needed', 'members_needed', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }