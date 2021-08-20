from django.shortcuts import render, redirect
from markdown2 import Markdown
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def info(request, title):

    content=util.get_entry(title)

    if(not content):
        return render(request, 'encyclopedia/error.html', {
            "status":"404",
            "message":"The requested page doesn't exist"
        })

    markdowner=Markdown()
    html_content=markdowner.convert(content)
    
    return render(request, "encyclopedia/info.html", {
        "title":title,
        "info":html_content
    })

def search(request):

    key=request.POST.get('q','')
    entries=util.list_entries()

    if key in entries:
        return redirect('info', title=key)
    
    suggest=[entry for entry in entries if not entry.find(key) == -1]
    return render(request, 'encyclopedia/index.html', {
        "entries":suggest
    })

def create(request):
    if request.method=="GET":
        return render(request, "encyclopedia/create.html")
    
    if request.method=="POST":
        input_title=request.POST.get('title', '')
        input_info=request.POST.get('info', '')

        if len(input_title)==0:
            return render(request, 'encyclopedia/error.html', {
            "status":"400",
            "message":"Please enter the title"
        })

        if util.get_entry(input_title):
            return render(request, 'encyclopedia/error.html', {
            "status":"400",
            "message":"This page already exists"
        })

        util.save_entry(input_title,input_info)
        return redirect('info', title=input_title)


def edit(request, title):
    if request.method=="GET":
        current_info=util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "md_info": current_info
            })

    if request.method=="POST":
        title=request.POST.get('title','')
        updated_info=request.POST.get('info','')
        
        util.save_entry(title,updated_info)
        return redirect('info', title=title)

def random(request):
    entries=util.list_entries()
    select=choice(entries)

    return redirect('info', title=select)





