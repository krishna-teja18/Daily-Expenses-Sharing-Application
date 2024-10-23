from django.urls import path
from .views import add_expense, user_expenses, overall_expenses, download_balance_sheet

urlpatterns = [
    path('add/', add_expense, name='add-expense'),
    path('user/<int:user_id>/', user_expenses, name='user-expenses'),
    path('overall/', overall_expenses, name='overall-expenses'),
    path('download/', download_balance_sheet, name='download-balance-sheet'),
]
