from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.models import Category, Wallet, Login_signup


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.GET.get('next')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"next": next_url})


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if Login_signup.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        Login_signup.objects.create(username=username, password=password)
        messages.success(request, "Account created! You can now log in.")
        return redirect("login")

    return render(request, "signup.html")


def test(request):
    return render(request, 'home-page.html')


@login_required
def income_view(request):
    print(f"User: {request.user}")
    print(f"Is Authenticated: {request.user.is_authenticated}")
    if request.method == "POST":
        amount = request.POST.get("amount", "").replace("$ ", "").strip()
        category_id = request.POST.get("category_id", "").strip()
        description = request.POST.get("description", "").strip()

        if not amount or not category_id:
            messages.error(request, "Amount and category are required.")
            return redirect('income')

        try:
            amount = Decimal(amount)
            category = Category.objects.get(pk=category_id)

            Wallet.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                description=description,
                type='income'
            )

            messages.success(request, "Income successfully added!")
            return redirect('home')

        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
        except InvalidOperation:
            messages.error(request, "Invalid amount format.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    categories = Category.objects.all()

    return render(request, "income.html", {"categories": categories})


@login_required
def home_view(request):
    user = request.user
    wallets = Wallet.objects.filter(user=user)

    total_income = sum(wallet.amount for wallet in wallets if wallet.type == 'income')
    total_expenses = sum(wallet.amount for wallet in wallets if wallet.type == 'expenses')
    balance = total_income - total_expenses

    return render(request, 'home-page.html', {
        'wallets': wallets,
        'balance': balance,
        'total_income': total_income,
        'total_expenses': total_expenses
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Wallet, Category


@login_required
def outcome_view(request):
    print(f"📌 Outcome View - User: {request.user}, Authenticated: {request.user.is_authenticated}")

    if request.method == "POST":
        amount = request.POST.get("amount", "").replace("$ ", "").strip()
        category_id = request.POST.get("category_id", "").strip()
        description = request.POST.get("description", "").strip()

        if not amount or not category_id:
            messages.error(request, "Amount and category are required.")
            return redirect('outcome')

        try:
            amount = Decimal(amount)
            category = Category.objects.get(pk=category_id)

            Wallet.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                description=description,
                type="expenses",
            )

            messages.success(request, "Expense successfully added!")
            return redirect('home')

        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    categories = Category.objects.all()
    return render(request, "outcome.html", {"categories": categories})
