import uuid
# Create your models here.
from django.db import models
from django.utils import timezone


class MoneySource(models.Model):
    SOURCE_CHOICES = [
        ('cash', 'Cash Account'),
        ('bank', 'Bank Account'),
        ('company_bank', 'Company Bank Account'),
    ]

    name = models.CharField(max_length=100)  # e.g., "Cash Account", "Bank Account"
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    source_type = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='cash')

    def __str__(self):
        return f"{self.name} ({self.source_type}) - Balance: {self.balance}"
    





class GeneralPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.TextField()  # To store notes about the payment
    source = models.ForeignKey(MoneySource, on_delete=models.CASCADE , default=None)
    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique payment token

    def __str__(self):
        return f" General Payment from {self.source.name} of {self.amount} on {self.date} - {self.note}"
    

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.source is None:
                # Set default source as cash if not provided
                self.source = MoneySource.objects.filter(source_type='cash').first()
                if self.source is None:
                    raise ValueError('No default cash source available')

            #if self.source.balance < self.amount:
              #  raise ValueError('Insufficient funds in source')
                
            # Update the balance
            self.source.balance -= self.amount
            self.source.save()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Restore the balance before deleting
        self.source.balance += self.amount
        self.source.save()
        super().delete(*args, **kwargs)






