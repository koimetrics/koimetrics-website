from django import forms
class SignupForm(forms.Form):
    
    full_name = forms.CharField(required=True, label="Full name")
    email = forms.EmailField(required=True, label="Email")
            
    password = forms.CharField(
        required=True, label="Password", 
        widget=forms.PasswordInput, min_length=8, strip=True
        )
            
    password_repeat = forms.CharField(
        required=True, label="Retype password", 
        widget=forms.PasswordInput, min_length=8, strip=True
        )

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if password != password_repeat:
            self._errors['password_repeat'] = self.error_class(['The passwords doesnt match'])

        return self.cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(
        required=True, label="Password", 
        widget=forms.PasswordInput, min_length=8, strip=True
        )

class UpdatePasswordForm(forms.Form):
    
    old_password = forms.CharField(
        required=True, label="Old password", 
        widget=forms.PasswordInput, min_length=8, strip=True
        )
    new_password1 = forms.CharField(
        required=True, label="New password", 
        widget=forms.PasswordInput, min_length=8, strip=True
        )
    new_password2 = forms.CharField(
        required=True, label="Repeat your new password", 
        widget=forms.PasswordInput, min_length=8, strip=True
        )

    def clean(self):
        super(UpdatePasswordForm, self).clean()
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            self._errors['new_password_repeat'] = self.error_class(['Passwords does not match'])
        return self.cleaned_data