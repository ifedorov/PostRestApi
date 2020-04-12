from rest_framework.routers import DefaultRouter
from starnavi_app import views

router = DefaultRouter()
router.register(r'post', views.PostViewSet)
router.register(r'user', views.UserCreateViewSet, basename='user')
urlpatterns = router.urls
