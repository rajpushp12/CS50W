from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def info(request, title):

    content=util.get_entry(title)

    if(not content):
        return HttpResponse("Error 404, the requested page doesn't exist")

    markdowner=Markdown()
    html_content=markdowner.convert(content)
    
    return render(request, "encyclopedia/info.html", {
        "title":title,
        "info":html_content
    })

def search(request):

    key=request.POST.get('q','')

    entries=util.list_entries()
    true=key in entries

    if true:
        return redirect('info', title=key)
    
    #filtered_entries=
    return render(request, 'encyclopedia/index.html')


