from rest_framework import filters, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from .authorization import TokenExpired
from .serializers import MovieSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserPermission
from movies.models import Movie


class Home(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title']
    ordering_fields = ['release_date', 'price']

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_order', 'date')
        sort_direction = self.request.GET.get('sort_direction', 'asc')
        search_query = self.request.GET.get('search', '')

        queryset = super().get_queryset()

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if sort_by == 'date':
            if sort_direction == 'asc':
                queryset = queryset.order_by('release_date')
            else:
                queryset = queryset.order_by('-release_date')
        elif sort_by == 'price':
            if sort_direction == 'asc':
                queryset = queryset.order_by('price')
            else:
                queryset = queryset.order_by('-price')

        return queryset


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsSuperUserPermission]
    authentication_classes = [TokenExpired, ]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['release_date', 'price']
    search_fields = ['title']

    def get_queryset(self):
        sort_order = self.request.query_params.get('sort_order', 'date')
        if sort_order == 'price':
            self.queryset = self.queryset.order_by('-price')
        else:
            self.queryset = self.queryset.order_by('release_date')
        return super().get_queryset()
