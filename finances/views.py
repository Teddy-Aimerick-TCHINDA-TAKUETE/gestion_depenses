from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExpenseForm, RevenueForm, RegisterForm
from .models import Expense, Revenue
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import TruncMonth
import calendar
import json

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
    mois = request.GET.get('mois')
    annee = request.GET.get('annee')
    categorie = request.GET.get('categorie')
    expenses = Expense.objects.filter(utilisateur=request.user)

    if categorie:
        expenses = expenses.filter(categorie=categorie)

    if mois:
        try:
            annee, mois = mois.split('-')
            expenses = expenses.filter(date__year=annee, date__month=mois)
        except ValueError:
            messages.error(request, "Format de date invalide.")
    elif annee:
        try:
            expenses = expenses.filter(date__year=annee)
        except ValueError:
            messages.error(request, "Année invalide.")

    return render(request, 'finances/expenses.html', {'expenses': expenses})

@login_required
def revenues(request):
    mois = request.GET.get('mois')
    annee = request.GET.get('annee')
    categorie = request.GET.get('categorie')
    revenues = Revenue.objects.filter(utilisateur=request.user)

    if categorie:
        revenues = revenues.filter(categorie=categorie)

    if mois:
        try:
            annee, mois = mois.split('-')
            revenues = revenues.filter(date__year=annee, date__month=mois)
        except ValueError:
            messages.error(request, "Format de date invalide.")
    elif annee:
        try:
            revenues = revenues.filter(date__year=annee)
        except ValueError:
            messages.error(request, "Année invalide.")

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

@login_required
def stats_view(request):
    mois = request.GET.get('mois')
    annee = request.GET.get('annee')

    expenses = Expense.objects.filter(utilisateur=request.user)
    revenues = Revenue.objects.filter(utilisateur=request.user)

    # Catégories Dépenses
    depenses_categorie = (
        expenses.values('categorie')
        .annotate(total=Sum('amount'))
        .order_by('categorie')
    )

    labels_cat_dep = [c['categorie'] for c in depenses_categorie]
    data_cat_dep = [float(c['total']) for c in depenses_categorie]

    # Catégories Revenus
    revenus_categorie = (
        revenues.values('categorie')
        .annotate(total=Sum('amount'))
        .order_by('categorie')
    )

    labels_cat_rev = [c['categorie'] for c in revenus_categorie]
    data_cat_rev = [float(c['total']) for c in revenus_categorie]

    if mois:
        annee_mois, mois_val = mois.split('-')
        expenses = expenses.filter(date__year=annee_mois, date__month=mois_val)
        revenues = revenues.filter(date__year=annee_mois, date__month=mois_val)

    elif annee:
        expenses = expenses.filter(date__year=annee)
        revenues = revenues.filter(date__year=annee)

    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_revenue = revenues.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_revenue - total_expense

    # Regrouper par mois
    monthly_expenses = (
        Expense.objects.filter(utilisateur=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    monthly_revenues = (
        Revenue.objects.filter(utilisateur=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Construire des tableaux de données
    labels = []
    revenus_par_mois = []
    depenses_par_mois = []

    mois_dict = {}

    for item in monthly_revenues:
        mois_label = item['month'].strftime('%B')
        mois_dict[mois_label] = {'revenus': item['total'], 'depenses': 0}

    for item in monthly_expenses:
        mois_label = item['month'].strftime('%B')
        if mois_label not in mois_dict:
            mois_dict[mois_label] = {'revenus': 0, 'depenses': item['total']}
        else:
            mois_dict[mois_label]['depenses'] = item['total']

    for mois in mois_dict:
        labels.append(mois)
        revenus_par_mois.append(float(mois_dict[mois]['revenus']))
        depenses_par_mois.append(float(mois_dict[mois]['depenses']))

    context = {
        'total_expense': total_expense,
        'total_revenue': total_revenue,
        'balance': balance,
        'labels': json.dumps(labels),
        'revenus_par_mois': json.dumps(revenus_par_mois),
        'depenses_par_mois': json.dumps(depenses_par_mois),
        'labels_cat_dep': json.dumps(labels_cat_dep),
        'data_cat_dep': json.dumps(data_cat_dep),
        'labels_cat_rev': json.dumps(labels_cat_rev),
        'data_cat_rev': json.dumps(data_cat_rev),
    }

    return render(request, 'finances/stats.html', context)