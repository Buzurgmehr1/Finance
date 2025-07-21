from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Income, Expense, Category
from django.db.models import Sum


def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        return get_object_or_404(User, id=user_id)
    return None


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")

        user = User.objects.create_user(username=username, email=email, password=password)
        request.session['user_id'] = user.id
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect('home')
        return HttpResponse("Invalid credentials")

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def home(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    return render(request, 'home.html',{'user':user})


def category_create_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    if request.method == "POST":
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('home')
    return render(request, 'category.html')


def category_edit_view(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        category.name = request.POST.get('name')
        category.save()
        return redirect('home')
    return render(request, 'category_edit.html', {'category': category})


def category_delete_view(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    category = get_object_or_404(Category, id=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('home')

    return render(request, 'category_delete.html', {'category': category})



def income_create_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    categories = Category.objects.all()
    if request.method == "POST":
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        category = get_object_or_404(Category, id=category_id)
        Income.objects.create(user=user, amount=amount, category=category, description=description)
        return redirect('home')
    return render(request, 'create_income.html', {'category': categories})


def income_edit_view(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    income = get_object_or_404(Income, id=pk, user=user)
    categories = Category.objects.all()
    if request.method == 'POST':
        income.amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        income.category = get_object_or_404(Category, id=category_id)
        income.description = request.POST.get('description')
        income.save()
        return redirect('home')
    return render(request, 'income_edit.html', {'income': income, 'category': categories})


def income_delete_view(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    income = get_object_or_404(Income, id=pk, user=user)
    income.delete()
    return redirect('home')


def expense_create_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    categories = Category.objects.all()
    if request.method == "POST":
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        category = get_object_or_404(Category, id=category_id)
        Expense.objects.create(user=user, amount=amount, category=category, description=description)
        return redirect('home')
    return render(request, 'create_expense.html', {'category': categories})


def expense_edit_view(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    expense = get_object_or_404(Expense, id=pk, user=user)
    categories = Category.objects.all()
    if request.method == 'POST':
        expense.amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        expense.category = get_object_or_404(Category, id=category_id)
        expense.description = request.POST.get('description')
        expense.save()
        return redirect('home')
    return render(request, 'expense_edit.html', {'expense': expense, 'category': categories})


def expense_delete_view(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    expense = get_object_or_404(Expense, id=pk, user=user)
    expense.delete()
    return redirect('home')


def summary_income_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    incomes = Income.objects.filter(user=user).order_by('-created_at')
    return render(request, 'summary_income.html', {'total_income': total_income, 'incomes': incomes, 'user': user})



def summary_expense_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    expenses = Expense.objects.filter(user=user).order_by('-created_at')
    return render(request, 'summary_expense.html', {'total_expense': total_expense, 'expenses': expenses, 'user': user})



def summary_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense
    return render(request, 'summary.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    })
