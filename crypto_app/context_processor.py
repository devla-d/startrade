from django.conf import settings
from .models import Transactions,Investments,POP



def user_investment_processor(request):
    user = request.user
    if user.is_authenticated:
        user_investment = Investments.objects.get(user=user)
        return {"user_investment": user_investment}
    else:
        return {"user_investment": "user_investment"}
