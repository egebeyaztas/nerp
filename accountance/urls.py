from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accountance_dashboard, name='accountance-dashboard'),
#INVOICES
    path('get-product-formset', views.add_formset_to_invoice, name='get-product-formset'),
    path('invoice-list', views.invoice_list, name='invoice-list'),
    path('invoice-list-expanded', views.invoice_list_expanded, name='invoice-list-expanded'),
    path('create-invoice', views.create_invoice, name='create-invoice'),
    path('edit-invoice/<str:invoice_id>', views.edit_invoice, name='edit-invoice'),
    path('delete-invoice/<str:invoice_id>', views.delete_invoice, name='delete-invoice'),
    path('hx/create-invoice-form', views.create_invoice_form, name='create-invoice-form'),
    path('hx/edit-invoice-form/<str:invoice_id>', views.edit_invoice_form, name='edit-invoice-form'),
#EXPENSES
    path('expense-list', views.expense_list, name='expense-list'),
    path('expense-list-expanded', views.expense_list_expanded, name='expense-list-expanded'),
    path('create-expense', views.create_expense, name='create-expense'),
    path('update-expense/<str:expense_id>', views.update_expense, name='update-expense'),
    path('delete-expense/<str:expense_id>', views.delete_expense, name='delete-expense'),
    path('hx/create-expense-form', views.create_expense_form, name='create-expense-form'),
    path('hx/update-expense-form/<str:expense_id>', views.update_expense_form, name='update-expense-form'),
#INCOMES
    path('income-list', views.income_list, name='income-list'),
    path('income-list-expanded', views.income_list_expanded, name='income-list-expanded'),
    path('create-income', views.create_income, name='create-income'),
    path('update-income/<str:income_id>', views.update_income, name='update-income'),
    path('delete-income/<str:income_id>', views.delete_income, name='delete-income'),
    path('hx/create-income-form', views.create_income_form, name='create-income-form'),
    path('hx/update-income-form/<str:income_id>', views.update_income_form, name='update-income-form'),
#BALANCE
    path('hx/update-balance-form/<str:balance_id>', views.update_balance_form, name='update-balance-form'),
    path('update-balance/<str:balance_id>', views.update_balance, name='update-balance'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)