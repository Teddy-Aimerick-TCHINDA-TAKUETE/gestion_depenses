from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExpenseForm, RevenueForm, RegisterForm
from .models import Expense, Revenue

def index(request):
    return render(request, 'finances/index.html')

def about(request):
    return render(request, 'finances/about.html')

def contact(request):
    return render(request, 'finances/contact.html')

def fonctionalites(request):
    return render(request, 'finances/fonctionalites.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès !")
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
        
    return render(request, 'finances/login.html')

def registre(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, "Inscription réussie, connectez-vous !")
            return redirect('login')
        else:
            messages.error(request, "Erreur d inscription. Vérifiez vos informations.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,"Erreur d inscription. Vérifiez vos informations. " + f"{field}: {error}")
    else:
        form = RegisterForm()
    return render(request, 'finances/registre.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description', '')

        Expense.objects.create(
            utilisateur=request.user,
            title=title,
            amount=amount,
            date=date,
            description=description
        )
        messages.success(request, "Dépense ajoutée avec succès !")
        return redirect('expenses')
    
    return render(request, 'finances/add_expense.html')

@login_required
def add_revenue(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description', '')

        Revenue.objects.create(
            utilisateur=request.user,
            title=title,
            amount=amount,
            date=date,
            description=description
        )
        messages.success(request, "Revenue ajoutée avec succès !")
        return redirect('revenues')
    
    return render(request, 'finances/add_revenue.html')

@login_required
def expenses(request):
    expenses = Expense.objects.filter(utilisateur=request.user)
    return render(request, 'finances/expenses.html', {'expenses': expenses})

@login_required
def revenues(request):
    revenues = Revenue.objects.filter(utilisateur=request.user)
    return render(request, 'finances/revenues.html', {'revenues': revenues})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    messages.success(request, "Dépense supprimée avec succès.")
    return redirect('expenses')

def delete_revenue(request, revenue_id):
    revenue = get_object_or_404(Revenue, id=revenue_id)
    revenue.delete()
    messages.success(request, "Revenu supprimé avec succès.")
    return redirect('revenues')

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Dépense modifiée avec succès.")
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'finances/edit_expense.html', {'form': form,'expense': expense, 'expense_id': expense_id})

def edit_revenue(request, revenue_id):
    revenue = get_object_or_404(Revenue, id=revenue_id)
    if request.method == "POST":
        form = RevenueForm(request.POST, instance=revenue)
        if form.is_valid():
            form.save()
            messages.success(request, "Revenu modifié avec succès.")
            return redirect('revenues')
    else:
        form = RevenueForm(instance=revenue)
    return render(request, 'finances/edit_revenue.html', {'form': form,'revenue': revenue, 'revenue_id': revenue_id})