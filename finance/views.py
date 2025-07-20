from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password
# Create your views here.


def get_current_user_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        return User.objects.filter(id=user_id).first()
    return None

def register_view(request):
    if request.method == "GET":
        return render(request, 'register.html')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")

        hashed_password = make_password(password)

        user = User.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            password=hashed_password
        )
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            request.session['user_id'] = user.id
            return redirect('home')
        return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def home(request):
    user = get_current_user_view(request)
    if not user:
        return redirect('login')
    return render(request,'home.html')
    

def category_create_view(request):
    user = get_current_user_view(request)
    if not user:
        return redirect('login')
    if request.method =="GET":
        return render(request, 'category.html')
    if request.method == "POST":
        name = request.POST.get('name',False)
    Category.objects.create(
        name = name
    )
    return redirect('home')


def income_create_view(request):
    user = get_current_user_view(request)
    if not user:
        return redirect('login')
    if request.method =="GET":
        categories = Category.objects.all()
        return render(request, 'create_income.html',{'category':categories})
    if request.method == "POST":
        amount = request.POST.get('amount',False)
        category = request.POST.get('category',False)
        description = request.POST.get('description',False)
        Income.objects.create(
            amount = amount,
            category = category,
            description = description,
            user = user
        )
        return redirect('home')
    
def income_edit_view(request, pk):
    user = get_current_user_view(request)
    if not user:
        return redirect('login')

    income = Income.objects.filter(id=pk, user=user).first()
    if not income:
        return HttpResponse("Income not found or access denied")

    if request.method == 'POST':
        income.amount = request.POST.get('amount',False)
        income.category = request.POST.get('category',False)
        income.description = request.POST.get('description',False)
        income.save()
        return redirect('home')

    return render(request, 'income_edit.html', {'income': income})

def expense_create_view(request):
    user = get_current_user_view(request)
    if not user:
        return redirect('login')
    if request.method =="GET":
        categories = Category.objects.all()
        return render(request, 'create_expense.html',{'category':categories})
    if request.method == "POST":
        amount = request.POST.get('amount',False)
        category = request.POST.get('category',False)
        description = request.POST.get('description',False)
        Expense.objects.create(
            amount = amount,
            category = category,
            description = description,
            user = user
        )
        return redirect('home')

def expense_edit_view(request, pk):
    user = get_current_user_view(request)
    if not user:
        return redirect('login')

    expense = Expense.objects.filter(id=pk, user=user).first()
    if not expense:
        return HttpResponse("Expense not found or access denied")

    if request.method == 'POST':
        expense.amount = request.POST.get('amount',False)
        expense.category = request.POST.get('category',False)
        expense.description = request.POST.get('description',False)
        expense.save()
        return redirect('home')

    return render(request, 'expense_edit.html', {'expense': expense})

