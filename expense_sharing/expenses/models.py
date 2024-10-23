from django.db import models
from users.models import User

class Expense(models.Model):
    class SplitMethod(models.TextChoices):
        EQUAL = 'EQUAL', 'Equal Split'
        EXACT = 'EXACT', 'Exact Amounts'
        PERCENTAGE = 'PERCENTAGE', 'Percentage Split'

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SplitMethod.choices, default=SplitMethod.EQUAL)

    def __str__(self):
        return f"Expense of {self.total_amount} by {self.creator}"

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_participants')
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # for exact splits
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # for percentage splits

    def __str__(self):
        return f"{self.participant.name} in {self.expense.total_amount}"
