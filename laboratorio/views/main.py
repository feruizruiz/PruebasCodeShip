from django.shortcuts import render


def index(request):
    context = {'mensaje': 'Hola Mundo'}
    return render(request, 'laboratorio/index.html', context)

