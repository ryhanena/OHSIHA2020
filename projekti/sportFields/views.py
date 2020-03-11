from django.shortcuts import render, redirect, get_object_or_404
from .forms import fieldForm
from .models import sportField
from django.views.generic import ListView, DetailView 

#Javatpoint?

class FieldListView(ListView):
    model = sportField
    template_name = 'sportFields/index.html'
    context_object_name = 'field_list'

    def get_queryset(self):
        return sportField.objects.all()


class FieldDetailView(DetailView):
    model = sportField
    template_name = 'sportFields/field_detail.html'

def create(request):
    if request.method == 'POST':
        form = fieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = fieldForm()

    return render(request, 'sportFields/create.html', {'form': form})


def edit(request, pk):
    field = sportField.objects.get(pk=pk)
    form = fieldForm(request.POST, instance=field)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'sportFields/edit.html', {'form':form})


def delete(request, pk):
    field = sportField.objects.get(pk=pk)
    field.delete()
    return redirect ("index")
