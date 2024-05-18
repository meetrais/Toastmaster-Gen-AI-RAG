from django.shortcuts import render
from django.http import HttpResponse, Http404
import requests

# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")


texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lecleo mi nec orci. Curabitur hendrerit, est in ",
        "Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim,  facilisis, dictum nunc ut, tincidunt diam.",
        "Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat ultricies"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")

def getapiresponse(request, user_text):
    ENVIRONMENT = 1
    PORT=str(5000)
    
    if ENVIRONMENT==1:
        BACKEND_SERVICE_ENDPOINT= "http://localhost:" + PORT
    elif ENVIRONMENT==2:
        BACKEND_SERVICE_ENDPOINT= "http://toastmaster-gen-ai-backend:" + PORT
    elif ENVIRONMENT==3:
        BACKEND_SERVICE_ENDPOINT= "https://tmbackendcontainerapp.nicesmoke-51dc90f5.southeastasia.azurecontainerapps.io"
    
    api = BACKEND_SERVICE_ENDPOINT
    api+= "/getresponse?user_text=" + user_text
    api+=  "&temperature=0.5"
    api+=  "&top_k=2"
    api+=  "&max_new_tokens=250"
    api+=  "&top_p=0.80"
    
    r = requests.get(api, params=request.GET)
    if r.status_code == 200:
        return HttpResponse(r)
    return HttpResponse('Something went wrong.')
    
    