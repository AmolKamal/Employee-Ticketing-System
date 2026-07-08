from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import EmployeeRegistrationForm, ContactInfoForm
from django.db import transaction
from django.contrib.auth.decorators import login_required

def register_employee(request):
    if request.method == 'POST':
        user_form = EmployeeRegistrationForm(request.POST)
        contact_form = ContactInfoForm(request.POST)
        
        if user_form.is_valid() and contact_form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=user_form.cleaned_data['username'],
                        password=user_form.cleaned_data['password']
                    )
                    
                    employee = user_form.save(commit=False)
                    employee.user = user
                    employee.save()
                    
                    contact = contact_form.save(commit=False)
                    contact.employee = employee
                    contact.save()
                    
                    return redirect('login')
            except Exception as e:
                user_form.add_error(None, "An error occurred while saving profile data. Please retry.")
    else:
        user_form = EmployeeRegistrationForm()
        contact_form = ContactInfoForm()
        
    return render(request, 'accounts/registration.html', {
        'user_form': user_form,
        'contact_form': contact_form
    })


@login_required
def dashboard_home(request):
    return render(request, 'accounts/dashboard.html')