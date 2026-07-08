from django import shortcuts, forms
from django.contrib.auth.models import User
from .models import EmployeeInfo, ContactInfo

class EmployeeRegistrationForm(forms.ModelForm):
    # Auth fields
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    # Model fields override for styling
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = EmployeeInfo
        fields = [ 'name', 'role', 'dob', 'gender', 'blood_group', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'id':'id_manager'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = EmployeeInfo.objects.exclude(role='DEVELOPER')

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['phone_number', 'email_address', 'local_address', 'permanent_address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +1234567890'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'}),
            'local_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class AdminEmployeeUpdateForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    # Bring in contact fields directly into the same update form
    phone_number = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    local_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    permanent_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

    class Meta:
        model = EmployeeInfo
        fields = ['name', 'role', 'dob', 'gender', 'blood_group', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prevent an employee from being assigned as their own manager
        if self.instance and self.instance.pk:
            self.fields['manager'].queryset = EmployeeInfo.objects.exclude(pk=self.instance.pk).exclude(role='DEVELOPER')