from django.db import models

from django.contrib.auth.hashers import make_password,check_password
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)


    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"

class Category(models.Model):
    name = models.CharField( max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = "Category"
        verbose_name_plural = "Categorys"



class Income(models.Model):
    user = models.ForeignKey(User, related_name='user_income', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    category = models.ForeignKey(Category, related_name='category_income', on_delete=models.CASCADE)
    description = models.CharField( max_length=200, null=True, blank=True)
    created_at = models.DateField( auto_now=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'income'
        managed = True
        verbose_name = "Income"
        verbose_name_plural = "Incomes"
class Expense(models.Model):
    user = models.ForeignKey(User, related_name='user_expense', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    category = models.ForeignKey(Category, related_name='category_expense', on_delete=models.CASCADE)
    description = models.CharField( max_length=200, null=True, blank=True)
    created_at = models.DateField( auto_now=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'expense'
        managed = True
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
