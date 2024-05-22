from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset token for {self.user.username}"
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField(null =False,blank=False)

    
    def __str__(self):
        return f'{self.user}'
