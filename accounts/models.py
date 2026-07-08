from django.db import models
from django.contrib.auth.models import User

class EmployeeInfo(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        DEVELOPER = 'DEVELOPER', 'Developer'

    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.DEVELOPER)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    # grade = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    
    manager = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='subordinates'
    )
    def save(self, *args, **kwargs):
        if not self.employee_id:
            prefix = ""
            if self.role == self.RoleChoices.DEVELOPER:
                prefix = "DEV"
            elif self.role == self.RoleChoices.MANAGER:
                prefix = "MNG"
            elif self.role == self.RoleChoices.ADMIN:
                prefix = "ADM"
            
            last_employee = EmployeeInfo.objects.filter(employee_id__startswith=prefix).order_by('-employee_id').first()
            
            if last_employee:
                try:
                    last_number = int(last_employee.employee_id[len(prefix):])
                    next_number = last_number + 1
                except ValueError:
                    next_number = 1
            else:
                next_number = 1
            
            self.employee_id = f"{prefix}{next_number:04d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.role})"


class ContactInfo(models.Model):
    employee = models.OneToOneField(
        EmployeeInfo, 
        on_delete=models.CASCADE, 
        related_name='contact_profile'
    )
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField(unique=True)
    local_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return f"Contact for {self.employee.name}"