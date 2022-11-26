from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'spybot'
urlpatterns = [
    path(r'', login_required(views.SpybotView.as_view()), name='spybot'),

    ]



