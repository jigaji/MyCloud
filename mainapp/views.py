from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewFolderForm
from .models import Folder
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    folders = request.user.folders.filter(folder=None)
    return render(request, 'home.html', {'folders':folders})

def create_new_folder(request):
    if request.method=='POST':
        if request.session['redirected_from'] is None:
            messages.error(request, 'Folder nit created')
            return redirect('mainapp:home')
        # POST request
        form = NewFolderForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user #current logged in user
            redirected_from = request.session['redirected_from'].split('/')
            if redirected_from[3] == '': #create new folder inside another folder
                pk =redirected_from[-2]
                form.folder = get_object_or_404(Folder, pk=pk)
            form.save()
            return HttpResponseRedirect(request.session['redirected_from'])
    else:
        # GET request
        request.session['redirected_from'] = request.META.get('HTTP_REFERER')
        createfolder = NewFolderForm()
    return render(request, 'createNewFolder.html',{
        'createfolder': createfolder
    })

def open_folder(request, pk):
    try:
        folder = get_object_or_404(Folder, pk=pk)
    except:
        messages.error(request, 'Folder does not exist')
        return redirect('mainapp:home')
    return render(request, 'openFolder.html', {
        'folder': folder
    })

     
