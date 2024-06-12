# views.py


from django.shortcuts import render


def index(request):
    content={}
    return render(
        request,
        "client/chatbot/index.html",context=content,
    )
