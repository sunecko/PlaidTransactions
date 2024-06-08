from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    tagged_as = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.description}"


class AccountInfo(models.Model):
    access_token = models.CharField(max_length=500, unique=True)
    item_id = models.CharField(max_length=500)

    def __str__(self):
        return "AccountInfo"
