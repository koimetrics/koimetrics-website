from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from connections.queries import get_website_key, sessions as website_sessions
from urllib.parse import urlparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from koimetrics.settings import API_HOST
# Create your models here.

class Website(models.Model):

    url = models.URLField(
        verbose_name= "Website full URL"
    )
    domain = models.CharField(
        verbose_name= "Website domain",
        max_length= 256, 
        blank= True, 
        null= True
    )
    apikey = models.CharField(
        verbose_name = "Website apikey",
        max_length = 255, 
        blank = True,
        null = True, 
    )

    URL_VERIFIED = "URL VERIFIED"
    SCRIPT_VERIFIED = "SCRIPT VERIFIED"
    status_choices = (("URL VERIFIED", URL_VERIFIED), ("SCRIPT VERIFIED", SCRIPT_VERIFIED))
    status = models.CharField(choices= status_choices, default= URL_VERIFIED, max_length= 256, blank= True, null= True)
    def new_website(url):
        ws = Website.objects.create(url= url)
        return ws
    def get_by_url(url):
        ws = Website.objects.filter(url= url).first()
        return ws
    def get_by_id(w_id):
        ws = Website.objects.filter(id = w_id ).first()
        return ws
    def get_by_apikey(apikey):
        ws = Website.objects.filter(apikey = apikey).first()
        return ws
    def koimetrics_script(self):
        script_url = API_HOST+"/API/v1/:key/koimetrics.js".replace(":key", self.apikey)
        return script_url
    def live_connections(self, seconds = 10):
        live_sessions = website_sessions(self.host(), self.apikey, seconds)
        return live_sessions
    def host(self):
        return self.url.split("//")[1].replace("www.", "").split("/")[0]
    def __str__(self):
        return self.url + ", " + self.analyst_set.first().user.email
    

@receiver(post_save, sender= Website)
def set_apikey(sender, instance, created, **kwargs):
    """set_apikey
    ====================================================== 
    description: when website is registered at first time, 
    set the apikey generated from remote API service.
    """
    if created:
        url = instance.url
        parsed_uri = urlparse(url)
        date_after_year = datetime.today()+ relativedelta(years=1)
        host     = parsed_uri.netloc.replace("www.", "")
        end_date = date_after_year.strftime("%Y-%m-%d")
        apikey   = get_website_key(host= host, end_date= end_date)
        instance.apikey = apikey
        instance.save()