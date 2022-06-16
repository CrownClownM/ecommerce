from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_viewsets import ProductViewSet
from apps.products.api.views.general_views import *

router = DefaultRouter()

router.register(r'products',ProductViewSet, basename = 'products') #Genera las rutas
router.register(r'measure-unit',MeasureUnitViewSet, basename = 'measure-unit')
router.register(r'indicators',IndicatorViewSet, basename = 'indicators')
router.register(r'category-products',CategoryProductViewSet, basename = 'category-products')

urlpatterns = router.urls #Se exportan las rutas y se mandan a la variable urlpatterns, es una lista de donde se sacan las rutas

