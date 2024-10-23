import csv
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from decimal import Decimal
from django.db.models import Sum

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_expense(request):
    data = request.data
    participants = data.get('participants')

    # Check if total amount and participants exist
    total_amount = Decimal(data.get('total_amount'))
    split_method = data.get('split_method')

    if split_method == 'EQUAL':
        num_participants = len(participants)
        split_amount = total_amount / num_participants
        for participant in participants:
            participant['amount'] = split_amount

    elif split_method == 'EXACT':
        total_split = sum([Decimal(participant.get('amount', 0)) for participant in participants])
        if total_split != total_amount:
            return Response({"error": "Exact amounts do not match the total amount."}, status=status.HTTP_400_BAD_REQUEST)

    elif split_method == 'PERCENTAGE':
        total_percentage = sum([Decimal(participant.get('percentage', 0)) for participant in participants])
        if total_percentage != 100:
            return Response({"error": "Percentages do not add up to 100%."}, status=status.HTTP_400_BAD_REQUEST)

        for participant in participants:
            percentage = Decimal(participant.get('percentage'))
            participant['amount'] = total_amount * (percentage / 100)

    serializer = ExpenseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_expenses(request, user_id):
    # Use expense_participants to filter by the participant user_id
    expenses = Expense.objects.filter(expense_participants__participant=user_id)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def overall_expenses(request):
    total_expenses = Expense.objects.aggregate(total_amount=Sum('total_amount'))
    return Response(total_expenses)

@api_view(['GET'])
def download_balance_sheet(request):
    # Collect expenses grouped by split_method
    equal_split_expenses = Expense.objects.filter(split_method='EQUAL')
    exact_split_expenses = Expense.objects.filter(split_method='EXACT')
    percentage_split_expenses = Expense.objects.filter(split_method='PERCENTAGE')

    # Calculate overall expenses
    overall_expenses = Expense.objects.aggregate(total_amount=Sum('total_amount'))

    # Prepare CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    
    # Function to write individual expenses
    def write_expenses(expenses, writer):
        for expense in expenses:
            participants = expense.expense_participants.all()
            for participant in participants:
                writer.writerow([
                    expense.creator.name, 
                    expense.total_amount, 
                    expense.split_method, 
                    participant.participant.name, 
                    participant.amount
                ])

    # Write headers for EQUAL split
    writer.writerow(['=== EQUAL SPLIT EXPENSES ==='])
    writer.writerow(['Creator', 'Total Amount', 'Split Method', 'Participant', 'Amount'])
    write_expenses(equal_split_expenses, writer)
    writer.writerow([])  # Empty row for better readability

    # Write headers for EXACT split
    writer.writerow(['=== EXACT SPLIT EXPENSES ==='])
    writer.writerow(['Creator', 'Total Amount', 'Split Method', 'Participant', 'Amount'])
    write_expenses(exact_split_expenses, writer)
    writer.writerow([])  # Empty row for better readability

    # Write headers for PERCENTAGE split
    writer.writerow(['=== PERCENTAGE SPLIT EXPENSES ==='])
    writer.writerow(['Creator', 'Total Amount', 'Split Method', 'Participant', 'Amount'])
    write_expenses(percentage_split_expenses, writer)

    # Write overall expenses at the end
    writer.writerow([])
    writer.writerow(['', '', '', 'Overall Expenses', overall_expenses['total_amount']])

    return response