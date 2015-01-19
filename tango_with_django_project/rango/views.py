from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': "Hey! I am bold from the context."}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')




	# return HttpResponse(make_html("Rango says here is the about page.<BR>"
     #                              "<A href=\"/rango/\">Back to /rango</A><BR>"
     #                              "<BR>"
     #                              "This tutorial has been put together by Tomasz Hippner, 2146437"))

# appends input string with html tags
# def make_html(str):
#     string_to_return = "<HTML><HEAD></HEAD><BODY>" + str + "</BODY></HTML>"
#     return string_to_return