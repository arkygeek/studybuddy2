from django.db import models

# Create your models here.
"""
This is where we are going to configure the database

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

"""
