from django.urls import path, include

from api.views.link import ListCreateLinks

urlpatterns = [
    path('links/', ListCreateLinks.as_view(), name='links-list-create')
]
