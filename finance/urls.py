from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('category-create',category_create_view,name='category'),
    path('create-income',income_create_view,name="income_create"),
    path('create-expense',expense_create_view,name="expense_create")
]
