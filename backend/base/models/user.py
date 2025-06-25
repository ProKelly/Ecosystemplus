from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ROLE_CHOICES = (
        ('user', 'User'),          # Farmer  
        ('community', 'Community') # Community admin
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_admin = models.BooleanField(default=False) 

    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

   
    @property
    def is_farmer(self):
        return self.role == 'user'
    
    @property
    def is_system_admin(self):
        return self.is_admin

    @property
    def is_community(self):
        return self.role == 'community'

    def __str__(self):
        return f"{self.get_full_name() if self.first_name else self.get_username()} ({self.role})"


class Community(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = {
        
    }
    
    admin = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name='administered_community',
        null=True,
        blank=True
    )
    
    name = models.CharField(max_length=255)
    email = models.EmailField()

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Optional

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

    @property
    def lat_lng(self):
        return f"{self.longitude}, {self.latitude}"

    def __str__(self):
        return f"{self.name} ({self.location})"


class AdminAccessRequest(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_requests')
    justification = models.TextField()
    reviewed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Access Request by {self.full_name} ({self.email}) - {'Approved' if self.approved else 'Pending'}"

    class Meta:
        verbose_name = 'Admin Access Request'
        verbose_name_plural = 'Admin Access Requests'
        ordering = ['-requested_at']