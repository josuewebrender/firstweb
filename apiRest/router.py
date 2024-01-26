from rest_framework.routers import DefaultRouter
from apiRest.views import apiRestViewSet

router_posts = DefaultRouter()
router_posts.register('', viewset=apiRestViewSet)
#urlpatterns=router_posts.urls