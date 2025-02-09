from tkinter.constants import CASCADE
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, DecimalField, ForeignKey, TextField, ImageField, URLField, Model, DateTimeField


class Login_signup(Model):
    username = CharField(max_length=100)
    password = CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expenses', 'Expenses')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - ${self.amount}"
