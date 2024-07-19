from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('reports/', views.reports, name='reports'),

    path('transactions_by_date_range/', views.transactions_by_date_range, name='transactions_by_date_range'),

]
