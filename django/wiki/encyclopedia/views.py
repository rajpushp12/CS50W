from django.shortcuts import render
from django.http import HttpResponse
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

