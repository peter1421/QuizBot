# views.py


from django.shortcuts import render


def index(request):
    content={}
    return render(
        request,
        "client/chapter/index.html",context=content,
    )
