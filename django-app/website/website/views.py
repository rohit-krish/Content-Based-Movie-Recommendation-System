from django.shortcuts import redirect


def reroute(request):
    return redirect("/browse")
