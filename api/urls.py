from django.urls import path 
from rest_framework.routers import DefaultRouter

from api.views import SendCodeApiView, CodeVerifyApiView, ResendCodeApiView, SignUpApiView, LoginAPIView, PostViewSet, CommentViewSet, MediaViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename='posts')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
	path('send-code/', SendCodeApiView.as_view()), 
	path('code-verify/', CodeVerifyApiView.as_view()),
	path('code-resend/', ResendCodeApiView.as_view()),
	path('signup/', SignUpApiView.as_view()),
	path('Login/', LoginAPIView.as_view()),
]

urlpatterns  += router.urls 