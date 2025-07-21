from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    # Аутентификация
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Категории
    path('category-create/', category_create_view, name='category_create'),
    path('category-edit/<int:pk>/', category_edit_view, name='category_edit'),
    path('category-delete/<int:pk>/', category_delete_view, name='category_delete'),

    # Доходы
    path('create-income/', income_create_view, name='income_create'),
    path('edit-income/<int:pk>/', income_edit_view, name='income_edit'),
    path('delete-income/<int:pk>/', income_delete_view, name='income_delete'),

    # Расходы
    path('create-expense/', expense_create_view, name='expense_create'),
    path('edit-expense/<int:pk>/', expense_edit_view, name='expense_edit'),
    path('delete-expense/<int:pk>/', expense_delete_view, name='expense_delete'),

    # Финансовая сводка
    path('summary/', summary_view, name='summary'),
    path('summary_income/', summary_income_view, name='summary_income'),
    path('summary_expense/', summary_expense_view, name='summary_expense'),
]
