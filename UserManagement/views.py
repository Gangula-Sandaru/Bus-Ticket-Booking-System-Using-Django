from django.shortcuts import render, redirect


# Create your views here.
def accountDashboard(request):
    return render(request, "UserManagement/ownerDashboard.html", {})


def logout(request):
    return redirect('adminView')
