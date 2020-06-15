from django import forms
from constants.constants import URL_REGEX

class WebsiteRegisterForm(forms.Form):

    url = forms.URLField(
        label= "Website url",
        widget= forms.URLInput(
            attrs= {
                "placeholder":"Ex: https://www.my-website.com",
                }
        )
    )