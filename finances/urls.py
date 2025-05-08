from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registre/', views.registre, name='registre'),
    path('fonctionalites/', views.fonctionalites, name='fonctionalites'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_revenue/', views.add_revenue, name='add_revenue'),
    path('expenses/', views.expenses, name='expenses'),
    path('revenues/', views.revenues, name='revenues'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('edit_revenue/<int:revenue_id>/', views.edit_revenue, name='edit_revenue'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('delete_revenue/<int:revenue_id>/', views.delete_revenue, name='delete_revenue'),
    path('statistiques/', views.stats_view, name='stats'),
]