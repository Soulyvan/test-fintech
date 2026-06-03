from django.urls import path

from .views import RegisterView, ViewAllAccountsView

urlpatterns = [
    path('', ViewAllAccountsView.as_view()),
    path("register/", RegisterView.as_view()),
]
