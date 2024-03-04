from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    first_str = request.GET.get('first_str', '')
    second_str = request.GET.get('second_str', '')
    result = first_str + second_str
    context = {
        'first_str': first_str,
        'second_str': second_str,
        'result': result,
    }
    return render(request, "requestapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, 'requestapp/user-bio-form.html', context=context)


def file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print("saved-file", filename)
            if myfile.size > 1048576:
                print(f"File size more than 1MB, File was deleted {myfile}")
                return render(request, 'requestapp/error-message.html')
    else:
        form = UploadFileForm()
    context = {
        "form": form,
    }

    return render(request, 'requestapp/file-upload.html', context=context)


