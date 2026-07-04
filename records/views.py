# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import SakeRecord
from .forms import SakeRecordForm


def sake_list(request):
    records = SakeRecord.objects.all()
    return render(request, "records/sake_list.html", {
        "title": '日本酒リスト',
        "records": records
    })

def sake_detail(request,pk):
    record = get_object_or_404(SakeRecord,pk=pk)
    return render(request, "records/sake_detail.html", {
        "title": "詳細",
        "record": record
    })

def sake_create(request):
    if request.method =="POST":
        form = SakeRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("sake:sake_list")
    else:
        form = SakeRecordForm()
    return render(request, "records/sake_create.html",{
        "title": "新規作成",
        "form": form
    })

def sake_update(request, pk):
    record = get_object_or_404(SakeRecord, pk=pk)
    if request.method == "POST":
        form = SakeRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect("sake:sake_detail", pk=record.pk)
    
    else:
        form = SakeRecordForm(instance=record)
    return render(request, "records/sake_update.html",{
        "title": "更新",
        "form": form
    })

def sake_delete(request, pk):
    record = get_object_or_404(SakeRecord, pk=pk)
    if request.method == "POST":
        record.delete()
        return redirect("sake:sake_list")
    return render(request, "records/sake_delete.html", {
        "title": "削除",
        "record": record
        })
