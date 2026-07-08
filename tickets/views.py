from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm, LeaveApplicationForm, TicketStatusForm
from .models import Ticket


@login_required
def raise_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Attach the employee raising the ticket
            ticket.raised_by = request.user.employee_profile
            ticket.ticket_type = 'COMPLAINT' 
            
            # The assigned_manager is pulled automatically from form.cleaned_data via form.save()
            ticket.save()
            
            messages.success(request, "Your complaint has been successfully submitted and routed!")
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



@login_required
def view_tickets(request):
    # Fetch all tickets raised by the current employee, newest first
    user_tickets = Ticket.objects.filter(
        raised_by=request.user.employee_profile
    ).order_by('-created_at')
    
    return render(request, 'tickets/view_tickets.html', {'tickets': user_tickets})

@login_required
def view_subordinate_tickets(request):
    user_profile = request.user.employee_profile
    if user_profile.role == 'ADMIN':
        all_tickets = Ticket.objects.all()
        return render(request, 'tickets/admin_view_ticket.html',{'tickets': all_tickets})
        
    if user_profile.role != 'MANAGER':
        messages.error(request, "Access denied. You do not have manager privileges.")
        return redirect('dashboard')
        
    managed_tickets = Ticket.objects.filter(
        assigned_manager=user_profile
    ).order_by('-created_at')
    
    return render(request, 'tickets/manager_view_tickets.html', {'tickets': managed_tickets})

@login_required
def ticket_detail(request, ticket_id):
    user_profile = request.user.employee_profile

    user_profile = request.user.employee_profile
    
    
    # Fetch the specific ticket or return a 404 page if it doesn't exist
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    
    # Security Guardrail: Only allow the explicitly assigned manager or an Admin to view/edit this
    if ticket.assigned_manager != user_profile and user_profile.role != 'ADMIN':
        messages.error(request, "Access denied. You are not authorized to view this ticket.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = TicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, f"Ticket #{ticket.ticket_id} status has been updated to {ticket.get_resolve_status_display()}!")
            return redirect('view_team_tickets')
    else:
        form = TicketStatusForm(instance=ticket)

    if user_profile.role == 'ADMIN':
        return render(request, 'tickets/admin_ticket_detail.html',{
        'ticket': ticket,
        'form': form
    })

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'form': form
    })