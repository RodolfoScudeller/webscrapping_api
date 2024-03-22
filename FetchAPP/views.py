from urllib.parse import urlparse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from pymongo import MongoClient
from bson import json_util, ObjectId


from FetchAPP.utils import get_website_info

# Create your views here.

@csrf_exempt
def fetchSiteApi(request): 
    if request.method == "POST":
        client = MongoClient('mongodb://your_username:your_password@localhost:27017/')

        db = client['analisesdb']

        collection = db['fetch_api']
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        _id = body_data.get('_id')
        obj_id = ObjectId(_id)
        print(obj_id)

        result = collection.find_one({"_id":obj_id})
        client.close()
        json_result = json.loads(json_util.dumps(result))

        return JsonResponse(json_result, safe=False)
@csrf_exempt
def saveSiteApi(request): 
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        
        body_data = json.loads(body_unicode)
        url = body_data.get('url')

        domain = url.split('/')[-2] 
        data_site = get_website_info(url)


        try:
            client = MongoClient('mongodb://your_username:your_password@localhost:27017/')
            
            db = client['analisesdb']
            
            collection = db['fetch_api']
            result = list(collection.find({"site_info.site_title": domain}))
            if(result):
                return JsonResponse({"success": False, "message": "Site ja salvo"}, status=500)
            else:
                result = collection.insert_one(data_site)
                client.close()
                return JsonResponse({"_id": str(result.inserted_id)}, status=201)
            
            
        except Exception as e:
            client.close()
            return JsonResponse({"success": False, "error": str(e)})

        


     