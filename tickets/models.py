from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import EmployeeInfo
from django.db import models

class Ticket(models.Model):
    class TicketType(models.TextChoices):
        COMPLAINT = 'COMPLAINT', 'Complaint'
        LEAVE = 'LEAVE', 'Leave Application'

    class StatusChoices(models.TextChoices):
        RAISED = 'RAISED', 'Raised'
        PROCESSING = 'PROCESSING', 'Processing'
        CLOSED = 'CLOSED', 'Closed'

    ticket_id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=20, choices=TicketType.choices, default=TicketType.COMPLAINT)
    
    # Title/Summary of the core issue
    title = models.CharField(max_length=200, default="General")
    detailed_issue = models.TextField()
    
    # Track the employee raising it using a Foreign Key link
    raised_by = models.ForeignKey(
        EmployeeInfo, 
        on_delete=models.CASCADE, 
        related_name='raised_tickets'
    )
    
    # The manager handling it (auto-assigned)
    assigned_manager = models.ForeignKey(
        EmployeeInfo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_tickets'
    )
    
    resolve_status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.RAISED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if not self.assigned_manager:
            if self.raised_by and self.raised_by.manager:
                self.assigned_manager = self.raised_by.manager
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.title} ({self.resolve_status})"