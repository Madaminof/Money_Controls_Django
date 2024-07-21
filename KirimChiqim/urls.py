from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),

    path('reports/', views.reports, name='reports'),

    path('transactions_by_date_range/', views.transactions_by_date_range, name='transactions_by_date_range'),
    path('api/daily-stats/', views.daily_stats, name='daily_stats'),
    path('api/weekly-stats/', views.weekly_stats, name='weekly_stats'),
    path('api/monthly-stats/', views.monthly_stats, name='monthly_stats'),

]
