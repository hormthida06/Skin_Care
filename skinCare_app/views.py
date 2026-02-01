from django.http import HttpResponse
from django.shortcuts import render

# def home(request):
#     return HttpResponse("Home page is working")
def home(request):
    return  render(request,"index.html")

def dashboard(request):
    return render(request, 'table/dashboard_body.html')