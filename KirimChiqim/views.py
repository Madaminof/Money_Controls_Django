from django.shortcuts import render, redirect

from .forms import TransactionForm
from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Transaction
from .forms import DateRangeForm

def index(request):
    transactions = Transaction.objects.all()
    total_income = sum(t.amount for t in transactions if t.type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.type == 'OUT')
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'index.html', context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

def reports(request):
    transactions = Transaction.objects.all()
    total_income = sum(t.amount for t in transactions if t.type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.type == 'OUT')
    balance = total_income - total_expense

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'reports.html', context)



def transactions_by_date_range(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            # Tekshirish: Sanalar to'g'ri formatda va end_date start_date'dan keyin bo'lishi kerak
            if start_date and end_date and start_date <= end_date:
                transactions = Transaction.objects.filter(date__range=[start_date, end_date])
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
