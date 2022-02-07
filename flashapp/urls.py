
from django.urls import path, include
from drip.admin import  drip_site

urlpatterns = [
    path('dripadmin/', drip_site.urls),
    path('',include("drip.urls"))
]
