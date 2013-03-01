from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from member.models import UserProfile
PLAYER_CLASSES = (('hunter', 'hunter'), ('engineer','engineer'), ('scout','scout'))

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    playerclass = forms.ChoiceField(required=True, choices=PLAYER_CLASSES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email 
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            profile = UserProfile(user=user, playerclass=self.cleaned_data['playerclass'], playername=user.username)
            profile.save()
        else:
            raise NotImplementedError("Can not create user with profile without commit")
        return user