from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Categories'


class HisobType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Hisob_type'


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('IN', 'Kirim'),
        ('OUT', 'Chiqim'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10,decimal_places=0)
    account = models.ForeignKey(HisobType,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.type} - {self.amount} - {self.account}"

    class Meta:
        db_table = 'Input_Output'


