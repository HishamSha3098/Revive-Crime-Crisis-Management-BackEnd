from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ReviveUser,Complaint,StaffApplication,Department
# Register your models here.


class ReviveUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'age', 'blood_group', 'marital_status', 'address','image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','is_admin', 'is_volunteer', 'groups', 'user_permissions')}),
    )
    list_display = ['email', 'name', 'phone', 'age', 'blood_group', 'marital_status', 'address']

admin.site.register(ReviveUser, ReviveUserAdmin)
admin.site.register(Complaint)
admin.site.register(StaffApplication)
admin.site.register(Department)




# admin.site.unregister(User)