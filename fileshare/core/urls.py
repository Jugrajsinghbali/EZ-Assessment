from django.urls import path
from .views import SignupView, VerifyEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import (
    FileUploadView,
    generate_download_link,
    download_file,
    FileListView,
)
urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='upload-file'),
    path('generate-download-link/<int:file_id>/', generate_download_link, name='generate-download-link'),
    path('download-file/<str:token>/', download_file, name='download-file'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += [
    path('list-files/', FileListView.as_view(), name='list-files'),
]
