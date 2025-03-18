from django.shortcuts import render
from django.http import JsonResponse

def constructor_view(request):
    return render(request, "constructor.html")

def save_stage(request):
    if request.method == "POST":
        return JsonResponse({"ok": 200}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)