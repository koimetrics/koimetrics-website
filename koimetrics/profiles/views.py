from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from profiles.forms import SignupForm, LoginForm
from profiles.models import Analyst
from django.contrib import messages
# Create your views here.
class SignUp(TemplateView):
    template_name = "web/signup.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SignUp, self).get_context_data(*args, **kwargs)
        context.update({"signup_form": SignupForm})
        return context
    
    def post(self, *args, **kwargs):
        signup_form = SignupForm(self.request.POST)
        if signup_form.is_valid():
            email = signup_form.cleaned_data.get("email")
            password = signup_form.cleaned_data.get("password")
            full_name = signup_form.cleaned_data.get("full_name")
            if not Analyst.get_by_email(email):
                Analyst.new_analyst(
                    email= email,
                    password= password,
                    full_name= full_name,
                )
                messages.success(self.request, "Your account has been created")
                return redirect("login")
            else:
                messages.error(self.request, "This account is already registered")
                return redirect("signup")

        
        else:
            return render(self.request, self.template_name, {"signup_form": signup_form})

class Login(TemplateView):
    template_name = "web/login.html"
    def get_context_data(self, *args, **kwargs):
        context = super(Login, self).get_context_data(*args, **kwargs)
        context.update({"login_form": LoginForm})
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return render(self.request, self.template_name, self.get_context_data())

    def post(self, *args, **kwargs):
        login_form = LoginForm(self.request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get("email")
            password = login_form.cleaned_data.get("password")
            user = authenticate(self.request, username= email, password= password)
            if user:
                login(self.request, user)
                return redirect("home")
        messages.error(self.request, "Invalid credentials")
        return redirect("login")