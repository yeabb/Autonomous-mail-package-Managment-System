from django.urls import path
from . import views
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path ("access", views.access, name="access"),
    path("open_box", views.open_box, name="open_box")
]