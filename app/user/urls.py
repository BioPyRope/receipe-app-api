from django.urls import path
from .views import CreateUserView,CreateTokenView,CreateUerManagerView

app_name="user" #CRITICAL!!

urlpatterns = [
    path('create/', CreateUserView.as_view(),name="create"),
    path('token/', CreateTokenView.as_view(),name="token"),
    path('me/', CreateUerManagerView.as_view(),name="me"),
    
    
    ]
