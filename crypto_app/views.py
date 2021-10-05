from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.http import JsonResponse
from django.utils import timezone 
from datetime import datetime, timedelta,date



from .models import Transactions,POP,Investments


def get_deadline():
	return datetime.today() + timedelta(days=1)

def home_view(request):
    return render(request, 'index.html')



def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')



def packages_view(request):
    return render(request, 'packages.html')





#dashboard
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def transactions_view(request):
    transactions_obj = Transactions.objects.filter(user=request.user)
    #transactions_obj = range(1, 50)
    page = request.GET.get('page', 1)
    paginator = Paginator(transactions_obj, 5)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    return render(request, 'transactions.html',{"transactions":transactions})


#dashboard
@login_required
def withdraw_view(request):
    if request.POST:
        user = request.user
        coin = request.POST.get('coin')
        amount = int( request.POST.get('amount'))
        wallet_address = request.POST.get('wallet_address')
        print(f"wallet_address : {wallet_address}, amount : {amount}, coin : {coin}")
        if user.balance > amount:
            if user.balance < 0:
                return JsonResponse({"msg":"Insufficient Balance"})
            else:
                transaction = Transactions.objects.create(user=user,trans_type="withdraw",wallet_address=wallet_address,amount_in_usd=amount,coin_tpye=coin,date=timezone.now())
                #user.balance -= amount
                #user.save()
                return JsonResponse({"msg":"Withdrawal Placed"})
        else:
            return JsonResponse({"msg":"Insufficient Balance"})
    return render(request, 'withdraw.html')


@login_required
def investments_view(request):
    investments = Investments.objects.get(user=request.user)
    print(investments.pop.status)
    return render(request, 'investments.html',{"investments":investments})



@login_required
def create_investments_view(request):
    if request.POST:
        user = request.user
        package = int(request.POST.get('package'))
        investments = Investments.objects.get(user=user)
        investments.amount_invested = package 
        investments.status = 'pending'
        investments.save()
        print(f"uri = {investments.uri}")
        return redirect(f"/new-investments/checkout/?investmenturi={investments.uri}&&investmentid={investments.id}")
    return render(request, 'create_investments.html')



@login_required
def create_investments_payment_checkout_view(request):
    if request.POST:
        user = request.user
        coin_tpye = request.POST.get('coin')
        transaction_id = request.POST.get('transaction_id')
        investment_id = int(request.POST.get('investment_id'))
        investment = get_object_or_404(Investments, id=investment_id)
        pop = POP.objects.create(user=user,transaction_id=transaction_id,coin_tpye=coin_tpye,amount_in_usd=investment.amount_invested,status="pending")
        investment.pop = pop
        investment.save()
        return redirect(f"/new-investments/payment/complete/?paymentID={pop.id}&&paymentURI={pop.uri}")
    else:
        id =  request.GET.get('investmentid')
        if id:
            investments = get_object_or_404(Investments,id=id)
            context = {
                'investment': investments
            }
            return render(request, 'create_investments_payment_checkout.html',context)
        else:
            return redirect('new-investments')


@login_required
def create_investments_payment_view(request):
    id = request.GET.get('paymentID')
    if id:
        pop = get_object_or_404(POP, id=id)
        return render(request, 'create_investments_payment.html',{"pop":pop})
    else:
        return redirect('new-investments')


def earnings(amount):
    return (7/100) * amount



def credit_daily_earning(request):
    if request.POST:
        user_id = request.POST.get('user_id')
        investment_id = request.POST.get('investment_id')
        user = request.user
        investment = Investments.objects.get(user=user)
        amount =  int(investment.amount_invested)
        investment.amount_earn += earnings(amount)
        investment.crediting_date = get_deadline()
        investment.save()
        user.balance += earnings(amount)
        user.save()
        return JsonResponse({"msg":"Account Credited"})
    else:
        return redirect('home')


def end_user_investment_view(request):
    if request.POST:
        user_id = request.POST.get('user_id')
        investment_id = request.POST.get('investment_id')
        user = request.user
        investment = Investments.objects.get(user=user)
        if investment.status == "completed":
            return JsonResponse({"msg":"Investment already ended"})
        else:
            investment.status = "completed"
            investment.save()
            return JsonResponse({"msg":"Investment  ended"})
    else:
        return redirect('home')