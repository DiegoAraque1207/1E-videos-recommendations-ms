from django.shortcuts import render
from django.http import HttpResponse
from service.models import UserPreferences
from service.models import VideoStatistics
import heapq
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt 

# Create your views here.
#def feedDbUser(request, user_id, category_id):
def feedDbUser(request):
    response = ""
    if request.method == 'POST':
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            user_id = json_data['id_user']
            category_id = json_data['id_category']
        
        except KeyError:
            return HttpResponse("Malformed data!")
    

    # user_id = 0
    # category_id = 1
    temp = UserPreferences.objects.filter(id_user = user_id).filter(id_category = category_id)
    if len(temp) == 0:
        user = UserPreferences(id_user = user_id, id_category = category_id)
        user.save()
        response = "New register"
    else:
        count = temp[0].counter
        count += 1
        temp[0].counter = count
        temp[0].save()
        response = "Data update"
    
    #return HttpResponse(response)
    return
@csrf_exempt 
def feedDbVideo(request):
    response = ""
    if request.method == 'POST':
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            video_id = json_data['id_video']
            category_id = json_data['id_category']
            score = json_data['score']
        
        except KeyError:
            return HttpResponse("Malformed data!")

    

    temp = VideoStatistics.objects.filter(id_video = video_id).filter(id_category = category_id)
    if len(temp) == 0:
        user = VideoStatistics(id_video = video_id, id_category = category_id, sumCalification = score)
        user.save()
        response = "New register"
    else:
        suma = temp[0].sumCalification
        suma += score
        temp[0].sumCalification = suma
        count = temp[0].num_views
        count += 1
        temp[0].num_views = count
        cali_count = temp[0].calicationsCount
        cali_count += 1
        temp[0].calicationsCount = cali_count
        temp[0].save()
        response = "Data update"

    #return HttpResponse(response)
    return

def searchRecommendations(request, user_id):
    response = ""
    #user_id = 0
    temp = UserPreferences.objects.filter(id_user = user_id)
    
    if len(temp) == 0:
        response = "There are no recommendations"
    else:
        categories = []
        heapq.heapify(categories)
        for i in range(len(temp)):
            heapq.heappush(categories,(((-1)*temp[i].counter), temp[i].id_category ))

        if len(categories) > 0:
            recomendations = []
            heapq.heapify(recomendations)
            for j in range(len(categories)):
                categorie = heapq.heappop(categories)
                print(categorie[1])
                temp = VideoStatistics.objects.filter(id_category = categorie[1])
                if len(temp) > 0:
                    for register in temp:
                        promedio = (register.sumCalification / register.calicationsCount) /  register.num_views
                        heapq.heappush(recomendations, (((-1) * promedio), ((-1) * register.num_views), register.id_video))
        if len(recomendations) > 0:
            temp_list = []
            while recomendations:
                temp_list.append(heapq.heappop(recomendations)[2])
            
            response = "{}".format(temp_list)

    return HttpResponse(response)
    