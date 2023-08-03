from django.contrib import admin
from .models import CrisisManage,EventManage,Wallet
# Register your models here.
admin.site.register(CrisisManage)
admin.site.register(EventManage)
admin.site.register(Wallet)