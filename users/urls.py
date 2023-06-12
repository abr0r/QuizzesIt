from django.urls import path

from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('profiles/', views.ProfilesView.as_view(), name='profiles'),
    path('landing/', views.LandingLoginView.as_view(), name='landingLogin'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.registerUser, name='register'),   
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('interest/<slug:interest_slug>', views.ProfilesByInterestView.as_view(), name='interest'),
    path('account/', views.UserAccountView.as_view(), name='account'),
    path('edit-account/', views.EditAccountView.as_view(), name='edit-account'),
    path('create-interest/', views.CreateInterestView.as_view(), name='create-interest'),
    path('update-interest/<slug:interest_slug>/', views.UpdateInterestView.as_view(), name='update-interest'),
    path('delete-interest/<slug:interest_slug>/', views.DeleteInterestView.as_view( ), name='delete-interest'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('message/<str:pk>/', views.ViewMessageView.as_view(), name='message'),
    path('create-message/<str:username>/', views.CreateMessageView.as_view(), name='create-message'),
    path('follow/<str:username>/', views.FollowUnfollowView.as_view(), name='follow-unfollow'),
]