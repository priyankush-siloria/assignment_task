from django.urls import path
from assignment_app.views import ApiLoginView, ApiLogoutView, RegistrationView, PostView

app_name = "assignment_app"

urlpatterns = [
    path('login', ApiLoginView.as_view(), name="login_token"),
    path('logout', ApiLogoutView.as_view(), name="logout"),
    path('register', RegistrationView.as_view(), name="Register"),
    path('post', PostView.as_view(), name="post"),
    path('post/<int:postid>', PostView.as_view(), name="post"),
]