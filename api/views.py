from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from core.models import Lead
from django.http import Http404
from api.serializer import LeadSerializer
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings
# from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView


# class LeadList(APIView):
#     pagination_class = LimitOffsetPagination
#     """
#     List all Leads, or create a new Lead.
#     """
#
#     def get(self, request, format=None):
#         leads = Lead.objects.all()
#         serializer = LeadSerializer(leads, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = LeadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadList(ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)



class LeadDetail(APIView):
    """
    Retrieve, update or delete a Lead instance.
    """
    def get_object(self, pk):
        try:
            return Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        lead = self.get_object(pk)
        serializer = LeadSerializer(lead)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        lead = self.get_object(pk)
        serializer = LeadSerializer(lead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lead = self.get_object(pk)
        lead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)