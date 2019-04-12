# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['fname']) < 2:
            errors['fname'] = 'First name needs to have more then 2 characters'

        if len(postData['lname']) < 2:
            errors['lname'] = 'Last name is too short. Needs to have at least two characters'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email needs to be a propper email address'

        # Check if email already exist!!!!
        # use .email to check the email cell in the DB!!!
        user1 = User.objects.filter(email=postData['email'])
        if len(user1):
            errors['email_exist'] = 'Use different email address'

        if len(postData['password']) < 8:
            errors['password'] = 'Password needs to have more then eigth characters'

        if postData['password'] != postData['c_pw']:
            errors['c_pw'] = 'Confirmation Password needs to match your Password'
        return errors

    def login_validator(self, postData):
        errors = {}

        # check if email matches regex requirements
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'

        # check if email is greater then 0. And compare with the len of the user mail addresses stored in the DB.
        user1 = User.objects.filter(email=postData['email'])
        if len(user1):
            # get all users with the email address and check
            # check if password matches the bcrypt password in the DB. don't forget variable.encode()) != True
            if bcrypt.checkpw(postData['password'].encode(), user1[0].password.encode()) is not True:
                errors['password'] = 'Password is not correct'
        else:
            errors['email_not_exists'] = 'No email address found you need to register first'
        return errors


class User(models.Model):
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return '<Object User: {} {} {} {}>'.format(self.fname, self.lname, self.email, self.password)


class Section(models.Model):
    name = models.CharField(max_length=60, default='no Name yet')
    desc = models.TextField(default='No description added')
    image = models.ImageField(default='static/easyLearn/mainPic.png', upload_to="media")
    progress = models.TextField(default='not started')
    order = models.IntegerField(default=0)


class Training(models.Model):
    name = models.CharField(max_length=60, default='no Name yet')
    desc = models.TextField(default='No description added')
    image = models.ImageField(default='static/easyLearn/mainPic.png', upload_to="media")
    sections = models.ManyToManyField(Section, related_name="trainings")
    user = models.ManyToManyField(User, related_name="userTrainings", default=0,)


class Activity(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=6, default='no Name yet')
    desc = models.TextField(default='No description added')
    order = models.IntegerField(default=0)


class TrainingProgress(models.Model):
    status = models.CharField(max_length=1, default='not started')
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SectionProgress(models.Model):
    status = models.CharField(max_length=1, default='not started')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ActivityProgress(models.Model):
    status = models.CharField(max_length=1, default='not started')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
