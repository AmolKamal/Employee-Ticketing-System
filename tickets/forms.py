from django import forms
from .models import Ticket
from accounts.models import EmployeeInfo

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'assigned_manager', 'detailed_issue']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Brief summary of your complaint...'
            }),
            # Added a specific HTML ID attribute for our JavaScript filter script to target
            'assigned_manager': forms.Select(attrs={
                'class': 'form-select', 
                'id': 'id_assigned_manager'
            }),
            'detailed_issue': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Provide complete details regarding the situation...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Baseline security filter: Strip out developers so they cannot be selected as managers
        self.fields['assigned_manager'].queryset = EmployeeInfo.objects.exclude(role='DEVELOPER')
        # Make the field required so a manager must be explicitly targeted
        self.fields['assigned_manager'].required = True

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