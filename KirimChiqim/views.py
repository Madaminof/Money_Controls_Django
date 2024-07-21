from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm, DateRangeForm
from datetime import timedelta
from django.utils.timezone import now

@login_required
def index(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    total_income = transactions.filter(type='IN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='OUT').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    category_expenses = (
        Transaction.objects
        .filter(user=user, type='OUT')
        .values('category__name')
        .annotate(total_amount=Sum('amount'))
        .order_by('category')
    )

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_expenses': category_expenses,
    }
    return render(request, 'index.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('index')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})




@login_required
def reports(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    total_income = sum(t.amount for t in transactions if t.type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.type == 'OUT')
    balance = total_income - total_expense

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'reports.html', context)

@login_required
def transactions_by_date_range(request):
    user = request.user
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if start_date and end_date and start_date <= end_date:
                transactions = Transaction.objects.filter(user=user, date__range=[start_date, end_date])
                total_income = sum(t.amount for t in transactions if t.type == 'IN')
                total_expense = sum(t.amount for t in transactions if t.type == 'OUT')
                balance = total_income - total_expense
            else:
                transactions = []
                total_income = total_expense = balance = 0
        except ValueError:
            transactions = []
            total_income = total_expense = balance = 0
    else:
        transactions = []
        total_income = total_expense = balance = 0

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'form': DateRangeForm(initial={'start_date': start_date_str, 'end_date': end_date_str}),
    }
    return render(request, 'kalendar.html', context)

@login_required
def daily_stats(request):
    user = request.user
    today = now().date()
    start_of_day = today
    end_of_day = start_of_day + timedelta(days=1)

    daily_income = Transaction.objects.filter(
        user=user, type='IN', date__range=[start_of_day, end_of_day]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0

    daily_expense = Transaction.objects.filter(
        user=user, type='OUT', date__range=[start_of_day, end_of_day]
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    daily_transactions = Transaction.objects.filter(
        user=user, date__range=[start_of_day, end_of_day]
    ).values('type', 'amount', 'description', 'date')

    return JsonResponse({
        'daily_income': daily_income,
        'daily_expense': daily_expense,
        'daily_transactions': list(daily_transactions)
    })

@login_required
def weekly_stats(request):
    user = request.user
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    weekly_income = Transaction.objects.filter(
        user=user, type='IN', date__range=[start_of_week, end_of_week]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0

    weekly_expense = Transaction.objects.filter(
        user=user, type='OUT', date__range=[start_of_week, end_of_week]
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    weekly_transactions = Transaction.objects.filter(
        user=user, date__range=[start_of_week, end_of_week]
    ).values('type', 'amount', 'description', 'date')

    return JsonResponse({
        'weekly_income': weekly_income,
        'weekly_expense': weekly_expense,
        'weekly_transactions': list(weekly_transactions)
    })

@login_required
def monthly_stats(request):
    user = request.user
    today = now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)

    monthly_income = Transaction.objects.filter(
        user=user, type='IN', date__range=[start_of_month, end_of_month]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0

    monthly_expense = Transaction.objects.filter(
        user=user, type='OUT', date__range=[start_of_month, end_of_month]
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    monthly_transactions = Transaction.objects.filter(
        user=user, date__range=[start_of_month, end_of_month]
    ).values('type', 'amount', 'description', 'date')

    return JsonResponse({
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_transactions': list(monthly_transactions)
    })

