from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from websites.models import Website

# Create your models here.

class Analyst(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
        )
    
    full_name = models.CharField(
        max_length = 256, 
        blank= True, 
        null=True
        )

    active = models.BooleanField(
        default= True
    )

    created_at = models.DateTimeField(
        default = timezone.now,
    )

    websites = models.ManyToManyField(Website, null = True)

    
    def new_website(self, url):
        ws = self.websites.create(url = url)
        return ws
    
    def get_by_url(self, url):
        return self.websites.filter(url = url).first()

    def get_by_email(email):
        return Analyst.objects.filter(user__email = email).first()
    
    def new_analyst(email, password, full_name):
        user = User.objects.create_user(
            username= email,
            password= password,
            email= email,
        )
        analyst = user.analyst
        analyst.full_name = full_name
        analyst.save()
        return analyst
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Analyst.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_analyst(sender, instance, **kwargs):
    instance.analyst.save()


