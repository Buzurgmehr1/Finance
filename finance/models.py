from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Income(models.Model):
    user = models.ForeignKey(User, related_name='incomes', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='income_categories', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    class Meta:
        db_table = 'income'
        verbose_name = "Income"
        verbose_name_plural = "Incomes"

class Expense(models.Model):
    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='expense_categories', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    class Meta:
        db_table = 'expense'
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
