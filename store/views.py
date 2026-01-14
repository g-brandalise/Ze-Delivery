from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from .models import Partner
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PartnerSerializer


class PartnerView(APIView):

        """
        Creates a new Partner

        Attributes: request

        Returns: Response
        """
    
    def post(self, request):

        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):

        lat = request.query_params.get('lat')
        long = request.query_params.get('long')

        if not lat or not long:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_point = Point(float(long), float(lat), srid=4326)
        except ValueError:
            return Response({"error": "Invalid coordinates"},  status=status.HTTP_400_BAD_REQUEST)


        partner = Partner.objects.filter(
        coverage_area__contains = user_point

        ).annotate(
        distance =  Distance('address', user_point)
        ).order_by(
        'distance'
        ).first()

        if partner:
            serializer = PartnerSerializer(partner)
            return Response(serializer.data)
        else:
            return Response({"error:": "Partner not attends here"} ,status=status.HTTP_404_NOT_FOUND)



class PartnerDetailView(APIView):

    def get(self, request, pk):
        """ Returns a Partner by their id """
        try:
            partner = Partner.objects.get(pk=pk)
            serializer = PartnerSerializer(partner)
            return Response(serializer.data)
        except Partner.DoesNotExist:
           return Response({"error":"partner not found"},status=status.HTTP_404_NOT_FOUND)


