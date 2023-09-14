from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=255)
    page = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title  

class Member(models.Model):
    name = models.CharField(max_length=255)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date_issued = models.DateTimeField(default=timezone.now)  # Add this field
    returned = models.BooleanField(default=False)
    rent_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Transaction {self.pk} - {self.book.title} - {self.member.name}"

