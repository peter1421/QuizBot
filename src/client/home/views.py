# views.py


from django.shortcuts import render


def index(request):
    return render(
        request,
        "client/home/index.html",
    )
