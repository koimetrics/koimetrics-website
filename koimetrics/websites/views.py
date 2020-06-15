from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from websites.forms import WebsiteRegisterForm
from websites.utils import check_website_contains_text, check_website_exists, website_contains_script
from websites.models import Website
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib import messages
from profiles.forms import UpdatePasswordForm
from django.contrib.auth import login
# Create your views here.

class Home(TemplateView):
    template_name = "dashboard/index.html"

class Register(TemplateView):
    template_name = "dashboard/websites/register.html"
    success_url = "websites-register"
    def get_context_data(self, *args, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context.update({"form": WebsiteRegisterForm()})
        return context
    
    def post(self, *args, **kwargs):
        analyst = self.request.user.analyst
        form = WebsiteRegisterForm(self.request.POST)
        ws = None
        if form.is_valid():
            url = form.cleaned_data.get("url")
            # check url exists
            if check_website_exists(url):
                ws = analyst.new_website(url= url) 
                return redirect( reverse('website-results') + "?url=%s" % (url))
        messages.error(self.request, f"We didn't received a response from {url}")
        return redirect(self.success_url)

class Results(TemplateView):
    template_name = "dashboard/websites/results.html"
    def get_context_data(self, *args, **kwargs):
        context = super(Results, self).get_context_data(**kwargs)
        website = self.request.user.analyst.get_by_url(self.request.GET.get("url"))
        if not website:
            raise Http404
        context.update({"website": website})
        return context

def check_script(request):
    if  request.POST.get("website"):
        w_id = int(request.POST.get("website"))
        website = Website.get_by_id( w_id )
        if not website:
            raise Http404
        if not website.analyst_set.first() == request.user.analyst:
            raise Http404
        
        # validate script
        if website_contains_script(website.url, website.koimetrics_script() ):
            website.status = website.SCRIPT_VERIFIED
            website.save()
        else:
            messages.error(request, "The script code couldn't be found in your website :(")
        return redirect( reverse('website-results') + "?url=%s" % (website.url))
    raise Http404
    

def check_connections(request):
    if request.POST.get("website"):
        w_id = int(request.POST.get("website"))
        website = Website.get_by_id( w_id )
        if not website:
            raise Http404
        if not website.analyst_set.first() == request.user.analyst:
            raise Http404
        
        connections = website.live_connections()
        return JsonResponse(connections, safe = False)

class AccountSettings(TemplateView):
    template_name = "dashboard/account-settings.html"
    success_url = "account-settings"
    def get_context_data(self, *args, **kwargs):
        context = super(AccountSettings, self).get_context_data(*args, **kwargs)
        context.update({"form": UpdatePasswordForm()})
        return context
    def post(self, *args, **kwargs):
        form = UpdatePasswordForm(self.request.POST)
        if form.is_valid():
            if self.request.user.check_password(form.cleaned_data.get("old_password")):
                self.request.user.set_password(form.cleaned_data.get("new_password1"))
                self.request.user.save()
                messages.success(self.request, "Your password has been reset")
                login(self.request, self.request.user)
            else:
                messages.error(self.request, "Your password didn't match")
        else:
            messages.error(self.request, "Passwords doesn't match")
        return redirect(self.success_url)

def remove(request):
    if request.POST:
        apikey  = request.POST.get("apikey")
        website = Website.get_by_apikey(apikey)
        if not website.analyst_set.first() == request.user.analyst:
            raise Http404
        website.delete()
    return redirect('home')