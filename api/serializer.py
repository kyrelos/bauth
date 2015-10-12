from rest_framework import serializers
from core.models import Lead
# from rest_framework_gis.serializers import GeoModelSerializer, GeoFeatureModelSerializer


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = (
            "id",
            "first_name", "last_name", "occupation", "monthly_income",
            "phone", "county", "nearest_town", "email"
        )


