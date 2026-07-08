from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm, LeaveApplicationForm

@login_required
def raise_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.raised_by = request.user.employee_profile
            ticket.ticket_type = 'COMPLAINT' 
            ticket.save()
            
            messages.success(request, "Your complaint has been successfully registered and routed to your manager!")
            return redirect('dashboard')
    else:
        form = ComplaintForm()
        
    return render(request, 'tickets/raise_complaint.html', {'form': form})

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Backend auto-mapping configuration
            ticket.raised_by = request.user.employee_profile 
            ticket.ticket_type = 'LEAVE'  # Classified explicitly as leave 
            
            # Append dates to description if you aren't using dedicated columns
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            ticket.detailed_issue += f"\n\n[Requested Leave Duration: {start} to {end}]"
            
            ticket.save() # Implicitly executes your auto-manager assignment logic 
            
            messages.success(request, "Leave request submitted successfully to your manager.")
            return redirect('dashboard')
    else:
        form = LeaveApplicationForm()
        
    return render(request, 'tickets/apply_leave.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket

@login_required
def view_tickets(request):
    # Fetch all tickets raised by the current employee, newest first
    user_tickets = Ticket.objects.filter(
        raised_by=request.user.employee_profile
    ).order_by('-created_at')
    
    return render(request, 'tickets/view_tickets.html', {'tickets': user_tickets})