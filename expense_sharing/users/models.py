from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    
    # Indian Mobile Number Validation
    mobile_number_regex = RegexValidator(regex=r'^\+?91?\d{10}$', message="Phone number must be entered in the format: '+919999999999'. Up to 10 digits allowed.")
    mobile_number = models.CharField(validators=[mobile_number_regex], max_length=13, unique=True)

    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
