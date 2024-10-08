from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    role_choices = (('LIBRARIAN', 'Librarian'), ('MEMBER', 'Member'),)
    role = models.CharField(max_length=12, choices=role_choices, default='MEMBER')
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='user groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_profile_groups",
        related_query_name="user_profile",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_profile_user_permissions',
        related_query_name='user_profile',
    )

    def __str__(self):
        return self.username

class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=12, default='AVAILABLE')

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="transaction_user",)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name="transaction_book",)
    issue_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    
    