from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField( max_length=100)


class Income(models.Model):
    user = models.ForeignKey(User, related_name='user_income', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    category = models.ForeignKey(Category, related_name='category_income', on_delete=models.CASCADE)
    description = models.CharField( max_length=200, null=True, blank=True)
    created_at = models.DateField( auto_now=True)
class Expense(models.Model):
    user = models.ForeignKey(User, related_name='user_expense', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    category = models.ForeignKey(Category, related_name='category_expense', on_delete=models.CASCADE)
    description = models.CharField( max_length=200, null=True, blank=True)
    created_at = models.DateField( auto_now=True)
