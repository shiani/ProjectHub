from django.urls import path
from .views import SignUp
app_name = 'user-api'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]