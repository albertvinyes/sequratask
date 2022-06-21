from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all, name='get_all'),
    path('merchant/<int:merchant>', views.get_by_merchant, name='get_by_merchant'),
]