from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import MovieForm
from .models import Movie
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect


class HomeListView(ListView):
    model = Movie
    template_name = 'movies/home.html'
    context_object_name = 'movies'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_order', 'date')
        sort_direction = self.request.GET.get('sort_direction', 'asc')
        queryset = super().get_queryset()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort_order', 'date')
        context['sort_by'] = sort_by
        return context


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_order', 'date')
        sort_direction = self.request.GET.get('sort_direction', 'asc')
        queryset = super().get_queryset()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort_order', 'date')
        context['sort_by'] = sort_by
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'


@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.created_by = request.user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/create_movie.html', {'form': form})


class MovieUpdateView(UpdateView):
    model = Movie
    template_name = 'movies/edit_movie.html'
    fields = ['title', 'release_date', 'duration', 'description']
    context_object_name = 'movie'
    success_url = reverse_lazy('movie_list')


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movies/movie_confirm_delete.html'
    context_object_name = 'movie'
    success_url = reverse_lazy('movie_list')

