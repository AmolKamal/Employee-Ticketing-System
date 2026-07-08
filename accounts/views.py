from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import EmployeeRegistrationForm, ContactInfoForm, AdminEmployeeUpdateForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import EmployeeInfo, ContactInfo
from tickets.models import Ticket

def homeView(request):
    return render(request, 'accounts/login.html')

@login_required
def register_employee(request):
    if request.user.employee_profile.role != 'ADMIN':
        return render(request ,'accounts/invalid.html')
    
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
def admin_dashboard(request):
    user_profile = request.user.employee_profile
    if user_profile.role == 'ADMIN':
        employee = EmployeeInfo.objects.all().exclude(role ='ADMIN')
        managers = EmployeeInfo.objects.filter(role='MANAGER').prefetch_related('subordinates')  
        unassigned_employees = EmployeeInfo.objects.filter(role='DEVELOPER', manager__isnull=True)  

        return render(request, 'accounts/admindash.html',{
        'managers': managers,
        'unassigned_employees': unassigned_employees
    })

@login_required
def dashboard_home(request):
    user_profile = request.user.employee_profile
    if user_profile.role == 'ADMIN':
        employee = EmployeeInfo.objects.all().exclude(role ='ADMIN')
        managers = EmployeeInfo.objects.filter(role='MANAGER').prefetch_related('subordinates')  
        unassigned_employees = EmployeeInfo.objects.filter(role='DEVELOPER', manager__isnull=True)  

        return render(request, 'accounts/admindash.html',{
        'managers': managers,
        'unassigned_employees': unassigned_employees
    })
    if user_profile.role == 'MANAGER':    
        subordinates = EmployeeInfo.objects.filter(
            manager=user_profile
        )
    else:
        subordinates = ""

    pending_tickets_count = Ticket.objects.filter(raised_by=user_profile).exclude(resolve_status='CLOSED').count() 


    context = {
        'subordinates':subordinates,
        'pending':pending_tickets_count,       
    }
    return render(request, 'accounts/dashboard.html',context)


@login_required
def admin_edit_employee(request, employee_id):
    if request.user.employee_profile.role != 'ADMIN':
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')

    employee = get_object_or_404(EmployeeInfo, employee_id=employee_id)
    # Safely get or create contact profile in case it doesn't exist
    contact, created = ContactInfo.objects.get_or_create(employee=employee)

    if request.method == 'POST':
        form = AdminEmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            with transaction.atomic():
                # Save core profile info
                updated_employee = form.save()
                
                # Save contact profile info pulled from custom form fields
                contact.phone_number = form.cleaned_data['phone_number']
                contact.email_address = form.cleaned_data['email_address']
                contact.local_address = form.cleaned_data['local_address']
                contact.permanent_address = form.cleaned_data['permanent_address']
                contact.save()
                
            messages.success(request, f"Profile for {employee.name} updated successfully.")
            return redirect('admin_dashboard')
    else:
        # Pre-populate the form with existing data from both tables
        initial_data = {
            'phone_number': contact.phone_number,
            'email_address': contact.email_address,
            'local_address': contact.local_address,
            'permanent_address': contact.permanent_address,
        }
        form = AdminEmployeeUpdateForm(instance=employee, initial=initial_data)

    return render(request, 'accounts/admin_edit_employee.html', {'form': form, 'employee': employee})


@login_required
def admin_delete_employee(request, employee_id):
    if request.user.employee_profile.role != 'ADMIN':
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')

    if request.method == 'POST':
        employee = get_object_or_404(EmployeeInfo, employee_id=employee_id)
        # Fetching the user model attached to this employee profile
        auth_user = employee.user
        
        # Deleting auth_user will cascade delete EmployeeInfo and ContactInfo
        auth_user.delete()
        
        messages.success(request, "Employee record dropped successfully.")
    return redirect('admin_dashboard')