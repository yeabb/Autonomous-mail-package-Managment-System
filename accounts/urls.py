from django.urls import path
from . import views
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path ("access", views.access, name="access"),
    path("open_box", views.open_box, name="open_box"),
    path("register", views.register, name="register"),
    path("verify_email", views.verify_email, name="verify_email"),
]