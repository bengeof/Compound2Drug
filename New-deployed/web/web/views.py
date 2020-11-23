from django.shortcuts import render
from run import *
from infer import *

# our home page view

# our home page view
def index(request):    
    return render(request, 'index.html')
    
    # custom method for generating predictions

# our result page view
def result(request):
    CID = int(request.GET['CID'])
    result = predict(CID)["predicted_pbdids"]

    return render(request, 'result.html', {'result':result})
    

