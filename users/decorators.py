from django.shortcuts import redirect


def user_login_required(function):
 def wrapper(request, login_url='xyz', *args, **kwargs):
  if not 'user' in request.session:
   return redirect("login")
  else:
   return function(request, *args, **kwargs)
 return wrapper


 
def verifiedaccount(function):
 def wrapper(request, login_url='xyz', *args, **kwargs):
  if not 'verified' in request.session:
   return redirect("profile")
  else:
   return function(request, *args, **kwargs)
 return wrapper