from django.urls import path, reverse_lazy

from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView

from .views import (
    CustomLoginView,
    CustomSignUpView,
    CustomResetPasswordView,
    ProfileUpdateView,
    ProfileDetailView,
)

app_name = 'profiles'
urlpatterns = [
    path('<int:id>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:id>/detail/', ProfileDetailView.as_view(), name='profile_detail'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('hangman:main_page')),  name='logout'),
    path('accounts/password-reset/', CustomResetPasswordView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', \
        PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html', success_url=reverse_lazy('profiles:password_reset_complete')), \
        name='password_reset_confirm'),
    path('accounts/password-reset-complete/', \
        PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), \
        name='password_reset_complete'),
]