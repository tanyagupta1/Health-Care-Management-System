from django.shortcuts import render

from django.http import HttpResponse
from .models import Post
# Create your views here.
# views alwas return http response or exception

posts = [
    {
        'author':'Tanya',
        'title':'Post 1',
        'content':' post 1 content',
        'date_posted': 'Aug 27,2018'
    },
    {
        'author':'Gupta',
        'title':'Post 2',
        'content':' post 2 content',
        'date_posted': 'Aug 29,2018'
    }
]

def home(request):
    context={
        'posts':Post.objects.all() # we can access the keys in our template 
    }
    # return HttpResponse('<h1>Blog home</h1>')
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title':"Blogs about"})