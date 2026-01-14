from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def about(request):
    return render(request, "pages/about.html")

@login_required
def membership(request):
    return render(request, "pages/membership.html")

def blog_single(request):
    return render(request, "pages/blog-single.html")

def policy(request):
    return render(request, "pages/policy.html")
