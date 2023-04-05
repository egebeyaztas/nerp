from django.shortcuts import render,redirect
from .forms import InvoiceForm, InvoiceLineFormSet, ExpenseForm, IncomeForm, BalanceForm
from .models import Invoice, InvoiceLine, Expense, Income, Balance
from general.models import Order
import time
from django.http import HttpResponse
from scripts.keygen import KeyGenerator

keygenerator = KeyGenerator()

class Route_data:
    def __init__(self):
        self.DASHBOARD = 'accountance-dashboard'

route = Route_data()

#Accounting Home
def accountance_dashboard(request):
    balance = Balance.objects.first()
    orders = Order.objects.all()
    balance_form = BalanceForm(instance=balance)
    income_form = IncomeForm()
    context = {
        'balance': balance,
        'balance_form': balance_form,
        'income_form': income_form,
    }
    return render(request, 'accountance/dashboard.html', context)

#Form Views

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'accountance/partials/invoice-list.html', {'invoices': invoices})

def invoice_list_expanded(request):
    invoices = Invoice.objects.all()
    return render(request, 'accountance/partials/invoice-list-expanded.html', {'invoices': invoices})

def create_invoice_form(request):
    form = InvoiceForm()
    formset = InvoiceLineFormSet()
    return render(request, 'accountance/partials/create-invoice-form.html', {'form': form, 'formset': formset})

def edit_invoice_form(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    form = InvoiceForm(instance=invoice)
    qs = invoice.lines.all()
    formset = InvoiceLineFormSet(instance=invoice, queryset=qs)
    context = {
        'form': form, 
        'formset': formset,
        'editview': True,
        'invoice': invoice,
    }
    return render(request, 'accountance/partials/create-invoice-form.html', context)

def add_formset_to_invoice(request):
    formset = InvoiceLineFormSet()
    return render(request, 'accountance/partials/product-formset.html', {'formset': formset})

#CRUD
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceLineFormSet(request.POST)
        print(formset.is_valid())
        print(form.is_valid())
        if form.is_valid() and formset.is_valid():
            obj_instance = form.save(commit=False)
            obj_instance.invoice_id = keygenerator.generate_unique_key('inv-')
            obj_instance.save()
            for form in formset:
                inline_obj = form.save(commit=False)
                inline_obj.invoice = obj_instance
                inline_obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'invoiceListChanged'})
        else:
            form = InvoiceForm()
            formset = InvoiceLineFormSet()
            context = {'form': form, 'formset': formset}
            return render(request, 'accountance/partials/create-invoice-form.html', context)

def edit_invoice(request, invoice_id):
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=invoice_id)
        form = InvoiceForm(request.POST, instance=invoice)
        qs = invoice.lines.all()
        formset = InvoiceLineFormSet(request.POST, queryset=qs, instance=invoice)
        print(form.is_valid())
        print(formset.is_valid())
        if form.is_valid() and formset.is_valid():
            obj_instance = form.save(commit=False)
            obj_instance.save()
            for form in formset:
                if form.cleaned_data != {}:
                    inline_obj = form.save(commit=False)
                    if inline_obj.invoice is None:
                        inline_obj.invoice = obj_instance
                    inline_obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'invoiceListChanged'})
        else:
            form = InvoiceForm()
            formset = InvoiceLineFormSet()
            context = {'form': form, 'formset': formset}
            return render(request, 'accountance/partials/edit-invoice-form.html', context)

def delete_invoice(request, invoice_id):
    
    invoice = Invoice.objects.get(id=invoice_id)
    invoice.delete()
    invoices = Invoice.objects.all()
    return render(request, 'accountance/partials/invoice-list.html', {'invoices': invoices})

#Generate Invoices and download them as PDF's.
def generate_invoice(invoice_id):
    pass

# ----------------------------------------------------------------

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'accountance/partials/expense-list.html', {'expenses':expenses})

def expense_list_expanded(request):
    expenses = Expense.objects.all()
    return render(request, 'accountance/partials/expense-list-expanded.html', {'expenses':expenses})

def create_expense_form(request):

    form = ExpenseForm()
    context = {'form': form, 'editview': False}

    return render(request, 'accountance/partials/expense-form.html', context)

def update_expense_form(request, expense_id):

    expense = Expense.objects.get(id=expense_id)
    form = ExpenseForm(instance=expense)
    context = {
        'form': form,
        'expense': expense,
        'editview': True
    }

    return render(request, 'accountance/partials/expense-form.html', context)

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'expenseListChanged'})
        else:
            form = ExpenseForm()
            context = {'form': form}
            return render(request, 'accountance/partials/expense-form.html', context)

def update_expense(request, expense_id):
    if request.method == 'POST':
        expense = Expense.objects.get(id=expense_id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'expenseListChanged'})
        else:
            form = ExpenseForm()
            context = {'form': form}
            return render(request, 'accountance/partials/expense-form.html', context)

def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    expense.delete()
    expenses = Expense.objects.all()
    return render(request, 'accountance/partials/expense-list.html',{'expenses':expenses})
    
# ----------------------------------------------------------------

def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'accountance/partials/income-list.html', {'incomes':incomes})

def income_list_expanded(request):
    incomes = Income.objects.all()
    return render(request, 'accountance/partials/income-list-expanded.html', {'incomes': incomes})

def create_income_form(request):
    form = IncomeForm()
    context = {'form': form, 'editview': False}

    return render(request, 'accountance/partials/income-form.html', context)

def update_income_form(request, income_id):
    income = Income.objects.get(id=income_id)
    form = IncomeForm(instance=income)
    context = {
        'form': form,
        'income': income,
        'editview': True
    }

    return render(request, 'accountance/partials/income-form.html', context)

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'incomeListChanged'})
        else:
            form = IncomeForm()
            context = {'form': form}
            return render(request, 'accountance/partials/income-form.html', context)

def update_income(request, income_id):
    if request.method == 'POST':
        income = Income.objects.get(id=income_id)
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'incomeListChanged'})
        else:
            form = IncomeForm()
            context = {'form': form}
            return render(request, 'accountance/partials/income-form.html', context)

def delete_income(request, income_id):
    income = Income.objects.get(id=income_id)
    income.delete()
    incomes = Income.objects.all()
    context = {'incomes': incomes}
    return render(request, 'accountance/partials/income-list.html', context)

#----------------------------------------------------------------

def update_balance_form(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    form = BalanceForm(instance=balance)
    context = {
        'form': form,
        'balance': balance,
        'editview': True
    }

    return render(request, 'accountance/partials/balance-form.html', context)

def update_balance(request, balance_id):
    if request.method == 'POST':
        balance = Balance.objects.get(id=balance_id)
        form = BalanceForm(request.POST, instance=balance)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger':'onBalanceChanged'})
        else:
            form = IncomeForm()
            context = {'form': form}
            return render(request, 'accountance/partials/balance-form.html', context)
    
