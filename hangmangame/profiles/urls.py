from django.urls import path, reverse_lazy

from .views import (
  ProfileUpdateView,
)

from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView

from profiles.views import (
    CustomLoginView,
    CustomSignUpView,
    CustomResetPasswordView,
)

app_name = 'profiles'
urlpatterns = [
    path('<int:id>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('hangman:main_page')),  name='logout'),
    # path('ajax/password-reset/', CustomResetPasswordView.as_view(), name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', \
    #     PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'), \
    #     name='password_reset_confirm'),
    # path('password-reset-complete/', \
    #     PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), \
    #     name='password_reset_complete'),
]