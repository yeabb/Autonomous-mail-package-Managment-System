from django.urls import path
from . import views
urlpatterns = [
    path("signupForm", views.signupForm, name="signupForm"),
    path("contact_email", views.contact_email, name="contact_email"),
    path ("login", views.login, name="login"),
    path ("personalAccount", views.personalAccount, name="personalAccount"),
    path("open_box", views.open_box, name="open_box"),
    #path("register", views.register, name="register"),
    path("verify_email", views.verify_email, name="verify_email"),
    path("sendEmailAgain", views.sendEmailAgain, name="sendEmailAgain"),
    path("email_reprompt", views.email_reprompt, name="email_reprompt"),
    path("finishup_registration", views.finishup_registration, name="finishup_registration"),
    path("staffBoxAccess", views.staffBoxAccess, name="staffBoxAccess"),
    path("addPackage", views.addPackage, name="addPackage"),
]