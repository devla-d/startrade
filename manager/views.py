from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.http import JsonResponse
from django.utils import timezone 
from datetime import datetime, timedelta,date
from django.conf import settings

from crypto_app.models import Transactions,POP,Investments
from account.models import Account
from .decorators import manager_required

 

@manager_required
def admin_dashboard_view(request):
    total_earnings = 0
    investments = Investments.objects.filter(status="active")
    for invest in investments:
        total_earnings += invest.amount_invested
    context = {
        "amount_invested" : total_earnings,
        "users" : Account.objects.all().count(),
        "pending_investment": Investments.objects.filter(status="pending").count()
    }
    return render(request, 'manager/dashboard.html',context)


@manager_required
def admin_dashboard_users_view(request):
    users = Account.objects.all()
    return render(request, 'manager/users.html',{'users':users})


@manager_required
def admin_dashboard_pop_view(request):
    pops = POP.objects.all().order_by('-date')
    return render(request, 'manager/pop.html',{"pops":pops})


@manager_required
def admin_dashboard_pop_detail_view(request, pk):
    pop = POP.objects.get(pk=pk)
    investment = Investments.objects.get(pop=pop)
    return render(request, 'manager/pop_detail.html',{"obj":pop, 'investment':investment})



def get_end_date():
	return datetime.today() + timedelta(days=7)

def get_crediting_date():
	return datetime.today() + timedelta(days=1)


def admin_dashboard_approve_pop_view(request):
    if request.POST:
        user_id = int(request.POST.get('user_id'))
        pop_id = int(request.POST.get('pop_id'))
        invest_id = int(request.POST.get('invest_id'))
        account = get_object_or_404(Account, pk=user_id)
        pop = get_object_or_404(POP, pk=invest_id)
        investment = get_object_or_404(Investments, pk=invest_id)
        pop.is_approved = True
        pop.approved_dated = timezone.now()
        pop.status = 'approved'
        pop.save()
        account.total_amount_invested += investment.amount_invested
        account.total_investement_count += 1
        account.save()
        investment.is_approved = True
        investment.end_date = get_end_date()
        investment.start_date = timezone.now()
        investment.crediting_date = get_crediting_date()
        investment.status = 'active'
        investment.save()
        return JsonResponse({"msg":"Payment Approved"})
    else:
        return JsonResponse({"msg":"Get Request Not Accepted"})



def admin_dashboard_decline_pop_view(request):
    if request.POST:
        user_id = int(request.POST.get('user_id'))
        pop_id = int(request.POST.get('pop_id'))
        invest_id = int(request.POST.get('invest_id'))
        account = get_object_or_404(Account, pk=user_id)
        pop = get_object_or_404(POP, pk=invest_id)
        investment = get_object_or_404(Investments, pk=invest_id)
        pop.status = 'declined'
        pop.save()
        return JsonResponse({"msg":"POP Declined"})
    else:
        return JsonResponse({"msg":"Get Request Not Accepted"})