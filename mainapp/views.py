from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewFolderForm
from .models import Folder, File
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from http import HTTPStatus

# Create your views here.
@login_required
def home(request):
    folders = request.user.folders.filter(folder=None)
    return redirect('mainapp:open_folder', pk=folders[0].pk)

def create_new_folder(request):
    if request.method=='POST':
        if request.session['redirected_from'] is None:
            messages.error(request, 'Folder not created')
            return redirect('mainapp:home')
        
        # POST request
        form = NewFolderForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user #current logged in user
            redirected_from = request.session['redirected_from'].split('/')
            if redirected_from[3] != '': #create new folder inside another folder
                pk =redirected_from[-2]
                form.folder = get_object_or_404(Folder, pk=pk)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, 'Folder already exists')
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


def upload_file(request):
    # 1. get file from request
    uploaded_file = request.FILES.get('uploadfile')
    # 2.  get folder - folder id
    folder_id = request.POST.get('fid')
    # 3. create new file object
    folder = get_object_or_404(Folder, pk=folder_id)
    File.objects.create(folder=folder, files=uploaded_file)
    # 4. redirect to openfilder.html with folderid
    return redirect('mainapp:open_folder', pk=folder_id)

def delete_file(request):
    pk = request.GET.get('pk')
    user = request.GET.get('user')

    try:
        if request.user.username != user:
            raise Exception('Unauthorized User')
        delfile = get_object_or_404(File, pk=pk)
        delfile.delete()
        return JsonResponse({
            delfile.filename:"Deleted",
            "status": HTTPStatus.OK
        })
    except Exception as e:
        return JsonResponse({
            "File": str(e),
            "status": HTTPStatus.NOT_FOUND
        })
    
def delete_folder(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    try:
        fid = folder.folder.pk
    except:
        return redirect("mainapp:home")
    else:   
        return redirect("mainapp:open_folder", pk=fid)
    finally:
        folder.delete()
    
