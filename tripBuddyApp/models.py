from django.db import models
from datetime import date
import re
import bcrypt

class UserManager(models.Manager):
    def register_validation(self, postData):
        errors = {}
        emailValidFormat = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])==0:
            errors['fnError'] = 'First name is required'
        elif len(postData['first_name'])<2:
            errors['fnError'] = 'First name is too short, must be at least 3 characters'
        elif postData['first_name'].isalpha()==False:
            errors['fnError'] = 'Names must be letters only'
        if len(postData['last_name'])==0:
            errors['lnError'] = 'Last name is required'
        elif len(postData['last_name'])<2:
            errors['lnError'] = 'Last name is too short, must be at least 3 characters'
        elif postData['last_name'].isalpha()==False:
            errors['lnError'] = 'Names must be letters only'
        if len(postData['user_email'])==0:
            errors['emailError'] = 'Email is required'
        elif not emailValidFormat.match(postData['user_email']):
            errors['emailError'] = 'Email is invalid, please use a valid email format'
        elif len(User.objects.filter(email=postData['user_email'])) != 0:
            errors['emailError'] = 'Email is already taken, please use a different email'
        if len(postData['user_pw'])==0:
            errors['pwError'] = 'Password is required'
        elif len(postData['user_pw'])<8:
            errors['pwError'] = 'Password is too short, must be at least 8 characters'
        if postData['confirm_pw'] != postData['user_pw']:
            errors['pwConf'] = 'Passwords do not match, please confirm with a matching password'
        return errors
    
    def login_validation(self, postData):
        errors = {}
        if len(User.objects.filter(email=postData['login_email'])) == 0:
            errors['loginEmailError'] = 'Not a registered email address'
        else:
            validUser = User.objects.get(email=postData['login_email'])
            if bcrypt.checkpw(postData['login_pw'].encode(), validUser.password.encode()) != True:
                errors['passwordError'] = 'Incorrect password'
        return errors

class TripManager(models.Manager):
    def new_trip_validation(self, postData):
        today = date.today()
        errors = {}
        if len(postData['trip_dest'])==0:
            errors['destError'] = 'Destination is blank'
        if postData['trip_start'] < str(today):
            errors['startError'] = 'Trip start date cannot be in the past'
        if postData['trip_end'] < postData['trip_start']:
            errors['endError'] = 'Trip cannot end before the start date'
        return errors

class User(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField(default='No Description Was Given')
    tripStart = models.DateField()
    tripEnd = models.DateField()
    organized_by = models.ForeignKey(User, related_name='leader', on_delete= models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()