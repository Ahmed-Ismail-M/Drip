from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from drip.models import User, Records

class DripAdmin(admin.AdminSite):
    site_header = 'Drip Database'

drip_site = DripAdmin(name='DripAdmin')
drip_site.register(User, UserAdmin)
drip_site.register(Records)