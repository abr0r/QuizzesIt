from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.views.generic import View

from .models import Profile, Interest
from .forms import CustomUserCreationForm, ProfileForm, InterestForm, MessageForm
from .utils import paginateObjects, searchProfiles


class LandingView(View):
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profiles')
        profiles, search_query = searchProfiles(request)
        custom_range, profiles = paginateObjects(request, 
            profiles, 3)
        context = {'profiles': profiles, 
        'search_query': search_query,
        'custom_range': custom_range}
        return render(request, self.template_name, context)


class LandingLoginView(View):
    #template_name = 'landing.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'There is no user with this username')
        user = authenticate(request, username=username, 
            password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' 
                in request.GET else 'account')
        else:
            messages.error(request, 'Invalid username or password')
        return redirect('landing')


class ProfilesView(View):
    template_name = 'users/profiles.html'

    def get(self, request, *args, **kwargs):
        profiles, search_query = searchProfiles(request)
        custom_range, profiles = paginateObjects(request, 
            profiles, 3)
        context = {'profiles': profiles, 
        'search_query': search_query,
        'custom_range': custom_range}
        return render(request, self.template_name, context)


class LoginUserView(View):
    template_name = 'users/login_register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account')
        return render(request, self.template_name)  

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'There is no user with this username')
        user = authenticate(request, username=username, 
            password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Invalid username or password')
        return redirect('login')


class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'You have been logged out')
        return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 
                'Аккаунт успешно создан!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request, 
                'Во время регистрации возникла ошибка')

    context = {'page': page, 'form': form}
    return render(request, 
        'users/login_register.html', context)


class UserProfileView(View):
    template_name = 'users/user-profile.html'

    def get(self, request, username, *args, **kwargs):
        profile = Profile.objects.get(username=username)
        interests = profile.interest_set.all()
        profiles = profile.follows.all()

        custom_range, profiles = paginateObjects(request, 
            profiles, 3)
        
        context = {'profile': profile, 'profiles': profiles,
                'interests': interests,
                'custom_range': custom_range}

        return render(request, 
            self.template_name, context)


class ProfilesByInterestView(LoginRequiredMixin, View):
    template_name = 'users/profiles.html'

    def get(self, request, interest_slug, *args, **kwargs):
        interest = Interest.objects.filter(slug__icontains=interest_slug)
        profiles = Profile.objects.exclude(user=request.user).distinct().filter(
            Q(interest__in=interest))
        context = {'profiles': profiles}

        return render(request, self.template_name, context)


class UserAccountView(LoginRequiredMixin,View):
    template_name = 'users/account.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        interests = profile.interest_set.all()
        profiles = profile.follows.all()
        custom_range, profiles = paginateObjects(request, 
            profiles, 3)

        context = {'profile': profile, 'profiles': profiles,
        'interests': interests, 'custom_range': custom_range}
        return render(request, self.template_name, context)


class EditAccountView(LoginRequiredMixin, View):
    template_name = 'users/profile_form.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, 
            instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        context = {'form': form}
        return render(request, self.template_name, context)


class CreateInterestView(LoginRequiredMixin, View):
    template_name = 'users/interest_form.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = InterestForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.description = request.POST.get('description')
            interest.profile = profile
            try:
                interest.save()
                messages.success(request, 'Interest has been added')
                return redirect('account')
            except IntegrityError:
                form.add_error('name', 'You already have an interest with this name and slug')

        context = {'form': form}
        return render(request, self.template_name, context)


class UpdateInterestView(LoginRequiredMixin, View):
    template_name = 'users/interest_form.html'

    def get(self, request, interest_slug, *args, **kwargs):
        profile = request.user.profile
        interest = profile.interest_set.get(slug=interest_slug)
        form = InterestForm(instance=interest)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, interest_slug, *args, **kwargs):
        profile = request.user.profile
        interest = profile.interest_set.get(slug=interest_slug)
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, 'The interest has been updated')
            return redirect('account')

        context = {'form': form}
        return render(request, self.template_name, context)


class DeleteInterestView(LoginRequiredMixin, View):
    template_name = 'delete_template.html'

    def get(self, request, interest_slug, *args, **kwargs):
        profile = request.user.profile
        interest = profile.interest_set.get(slug=interest_slug)
        context = {'object': interest}
        return render(request, self.template_name, context)

    def post(self, request, interest_slug, *args, **kwargs):
        profile = request.user.profile
        interest = profile.interest_set.get(slug=interest_slug)
        if request.method == 'POST':
            interest.delete()
            messages.success(request, 'The interest has been deleted')
            return redirect('account')

        context = {'object': interest}
        return render(request, self.template_name, context)


class InboxView(LoginRequiredMixin, View):
    template_name = 'users/inbox.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        messageRequests = profile.messages.all()
        unreadCount = messageRequests.filter(is_read=False).count()
        context = {'messageRequests': messageRequests, 
        'unreadCount': unreadCount}
        return render(request, self.template_name, context)


class ViewMessageView(LoginRequiredMixin, View):
    template_name = 'users/message.html'

    def get(self, request, pk, *args, **kwargs):
        profile = request.user.profile
        message = profile.messages.get(id=pk)
        if message.is_read is False:
            message.is_read = True
            message.save()
        context = {'message': message}
        return render(request, self.template_name, context)


class CreateMessageView(LoginRequiredMixin, View):
    template_name = 'users/message_form.html'

    def get(self, request, username, *args, **kwargs):
        recipient = Profile.objects.get(username=username)
        form = MessageForm()

        try:
            sender = request.user.profile
        except:
            sender = None

        context = {'recipient': recipient, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, username, *args, **kwargs):
        recipient = Profile.objects.get(username=username)
        form = MessageForm(request.POST)

        try:
            sender = request.user.profile
        except:
            sender = None

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 
                'Сообщение успешно отправлено!')
            return redirect('user-profile', 
                username=recipient.username)

        context = {'recipient': recipient, 'form': form}
        return render(request, self.template_name, context)


class FollowUnfollowView(LoginRequiredMixin, View):
    def get(self, request, username, *args, **kwargs):
        profile = Profile.objects.get(username=username)
        if request.method == 'POST':
            current_user_profile = request.user.profile
            data = request.POST
            action = data.get('follow')
            if action == 'follow':
                current_user_profile.follows.add(profile)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == 'unfollow':
                current_user_profile.follows.remove(profile)
            current_user_profile.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))