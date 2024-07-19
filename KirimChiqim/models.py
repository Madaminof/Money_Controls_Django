from django.db import models


class Transaction(models.Model):
    ACCOUNT_TYPES = (
        ('cash', 'Naqd Pul'),
        ('card', 'Karta'),
        ('currency', 'Valuta'),
    )

    TRANSACTION_TYPES = (
        ('IN', 'Kirim'),
        ('OUT', 'Chiqim'),
    )

    CATEGORIES = (
        ('transport', 'Transport'),
        ('food', 'Oziq-ovqat'),
        ('entertainment', 'Ko\'ngil ochar'),
    )

    date = models.DateField()
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.type} - {self.amount} - {self.account}"

    class Meta:
        db_table = 'kirim_chiqim'


