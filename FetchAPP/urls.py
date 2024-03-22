from FetchAPP import views
from django.urls import path, re_path, include

urlpatterns = [ 
    path('salve-info', views.saveSiteApi),
    path('get_info', views.fetchSiteApi),
]
