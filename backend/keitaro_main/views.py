from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json




user_ids = {'bogdan': 1799244985, 'lovelas': 1836086969} 
# Create your views here.

@csrf_exempt
def check_id(request):
	user_id_input = int(request.body.decode("utf-8"))
	key_list = list(user_ids.keys())
	val_list = list(user_ids.values())
	if user_id_input in val_list:
		position = val_list.index(user_id_input)
		print(key_list[position])
		data = json.dumps({"id_status": True, "login": key_list[position]})
	else:
		data = json.dumps({"id_status": False})
	return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_bot(request):
	user_data_input = json.loads(request.body)
	user = User.objects.create_user(username = user_data_input['login'], password = user_data_input['password'])
	return HttpResponse(json.dumps({"reg_status": True}), content_type='application/json')

def profile_page(request):
	return render(request, "profile.html")