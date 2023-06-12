from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, FileInput

from .models import Profile, Interest, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 
        'password1', 'password2']
        labels = {
            'first_name': 'Name and Surname',
            'email': 'Email', 
            'username':'Login', 
            'password1':'Password', 
            'password2': 'Confirm password'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                'summary', 'about', 'image', 
                'city', 'profession',
                'github', 'linkedin', 'twitter',
                'youtube']
        labels = {
            'name': 'Name and Surname',
            'email': 'Email', 
            'username':'Login',
            'city': 'City', 
            'profession': 'Profession',
            'summary': 'Summary about you',
            'about': 'About yourself (hobbies, interests, etc.)',
            'image': 'Change profile photo',
        }
        widgets = {
            'image': FileInput(),
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})
                

class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = '__all__'
        exclude = ['profile', 'slug']

        labels = {
            'name': 'Name',
            'description':'Description',
        }

    def __init__(self, *args, **kwargs):
        super(InterestForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})




class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = {'name': 'Name and Surname',
            'email': 'Email', 
            'subject':'Theme',
            'body':'Message text'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})
