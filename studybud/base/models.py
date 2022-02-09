# Create your models here.
""" By default, the db cannot have an instance of something without having
      a value for every entry, so we set null to equal true so that we _can_
      have an empty entry here. name, for example, cannot be empty. Likewise,
      blank form is ok.
      """
""" This is where we are going to configure the database

We are going to create Python classes.
The classes we create represent the database tables.

Python Class
(Inherits from Django Models)

class Project(models.Model):
      title = models.CharField()
      description = models.TextField()
      id = models.UUIDField()

The above will create a table in the database called project
and every attribute inside of that Python class will represent a column
inside of the database.

      Project Database Table
      ID    TITLE       DESC
      1     ...         ...        <-- each row is like an instance of a class
      2     ...         ...
      3     ...         ...
      4     ...         ...
      5     ...         ...
      ...

The classes are like models of the database, so that's why it's called models.py

"""


from os import O_NDELAY
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
      name = models.CharField(max_length=200)

      def __str__(self):
          return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
