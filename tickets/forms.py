from django import forms
from .models import Ticket

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'detailed_issue']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Brief summary of your complaint...'
            }),
            'detailed_issue': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Provide complete details regarding the situation...'
            }),
        }

class LeaveApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Ticket
        fields = ['title', 'detailed_issue']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Annual Sick Leave Request'
            }),
            'detailed_issue': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Provide a brief explanation for your leave request...'
            }),
        }