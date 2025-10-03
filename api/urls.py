from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserInfoView.as_view(), name='user_info'),
    path('user/logros/', views.UserLogrosView.as_view(), name='user_logros'),
    path('user/game/partidas/', views.UserGamePartidasView.as_view(), name='user_game_partidas'),
    path('user/game/stats/', views.UserGameStatsView.as_view(), name='user_game_stats'),
]