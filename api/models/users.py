import uuid

from django.utils import timezone
from django.db import models 
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt import tokens

from api.utilits import generate_pin

NEW, VERIFIED, DONE = ('new', 'verified', 'done')
class User(AbstractUser): 
  status_choices  = (
    (NEW, NEW),
    (VERIFIED, VERIFIED), 
    (DONE, DONE),
  )
  phone = models.CharField(max_length=13,  null=True, blank=True)
  status = models.CharField(max_length=20, choices=status_choices, default=NEW)
  bio = models.TextField(null=True, blank=True)
  image  = models.FileField(upload_to='images/', null=True, blank=True)

  def  __str__(self):
    return self.username
  
  def create_code(self): 
    code = generate_pin()
    UserConfirmation.objects.create(
      user = self,
      code  = code
    )
    return code
  
  def save(self, *args, **kwargs):
    if not self.username:
        user_uuid = str(uuid.uuid4()).split('-')[-1]
        self.username = f'user{user_uuid}'

    if not self.password:
        random_uuid = str(uuid.uuid4()).split('-')[-1]
        self.set_password(f'user{random_uuid}')

    super().save(*args, **kwargs)


  def token(self):
    refresh = tokens.RefreshToken.for_user(self)
    return  {'acces': str(refresh.access_token), "refresh": str(refresh)}
  

class UserConfirmation(models.Model): 
  code = models.CharField(max_length=6)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmations')
  expired_at = models.DateTimeField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    if not self.pk:
        self.expired_at = timezone.now() + timezone.timedelta(minutes=2)
    super().save(*args, **kwargs)

  
  def is_expired(self):
    return self.expired_at < timezone.now()
  
  def __str__(self):
    return f"{self.user.username}|  {self.code}"