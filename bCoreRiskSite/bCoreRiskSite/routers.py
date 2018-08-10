from rest_framework import routers
from bCoreRiskApp.viewsets import (
    RiskSerializerViewSet,
    RiskFieldSerializerViewSet,
    ChoiceSerializerViewSet
)

router = routers.DefaultRouter()
router.register(r'risk', RiskSerializerViewSet)
router.register(r'riskfield', RiskFieldSerializerViewSet)
router.register(r'choice', ChoiceSerializerViewSet)
