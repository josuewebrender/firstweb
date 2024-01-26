from rest_framework.routers import DefaultRouter
from scoopsalud.views import scoopsaludViewSet

router_posts = DefaultRouter()
router_posts.register('', viewset=scoopsaludViewSet)
#urlpatterns=router_posts.urls