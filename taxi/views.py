from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import Car, Manufacturer  # mantenha Car/Manufacturer importados normalmente
from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm

UserModel = get_user_model()  # dinâmico: suporta custom user model


@login_required
def index(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    context = {"num_visits": num_visits}
    return render(request, "taxi/index.html", context)


# Car views (mantidas, com Car import normal)
class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    queryset = Car.objects.select_related("manufacturer").prefetch_related("drivers")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        user = request.user
        # use user (instância do UserModel) para adicionar/remover dos drivers do carro
        if user in car.drivers.all():
            car.drivers.remove(user)
        else:
            car.drivers.add(user)
        return redirect("taxi:car-detail", pk=pk)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


# Driver views — usando UserModel como model
class DriverListView(LoginRequiredMixin, generic.ListView):
    model = UserModel
    template_name = "taxi/driver_list.html"
    context_object_name = "driver_list"

    def get_queryset(self):
        # se houver filtro (ex.: apenas users com driver profile), aplique aqui
        return UserModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        # CORREÇÃO: comparar objetos do mesmo tipo (user == user)
        for driver in context["driver_list"]:
            driver.is_current_user = (driver == current_user)
        return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserModel
    template_name = "taxi/driver_detail.html"
    context_object_name = "driver"


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserModel
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserModel
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserModel
    success_url = reverse_lazy("taxi:driver-list")
