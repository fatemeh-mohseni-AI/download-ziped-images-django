import os , datetime
from django.http import HttpResponse
import json 

from django.http import HttpResponse
import requests
from PIL import Image
from io import BytesIO
import zipfile

def image_list(request , day):
 
# Get the list of all files and directories
    path = f"/media/pic/{day}"
    try:
        dir_list = os.listdir(path)
        json_stuff = json.dumps({f"/media/pic/{day}/" : dir_list})    

        return HttpResponse(json_stuff, content_type ="application/json")
    except:
        path = "/media/pic/"
        dir_list = os .listdir(path)
        return HttpResponse(f"there is no photo for chosen date .\nchoices are : {dir_list}")
    
# -------------------------------------------------------------------------   
def fetch_image(url):
    ''' function to return pil image'''
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def get_image_buffer(image):
    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    return img_buffer


def generate_zip(list_of_tuples):
    ''' function to write zip file'''
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in list_of_tuples:
            zf.writestr(f[0], f[1].read())
    return mem_zip.getvalue()


def download_to_zip(request, date):
    images_tuple = []

    path = f"/media/pic/{date}/"
    dir_list = os.listdir(path)
    images = [path+image for image in dir_list]
    print(images)
    count = 0
    try:
        for i in images:
            url = 'http://127.0.0.1:8000'+i
            images_tuple.append(
                ("image" + str(count) + ".jpg", get_image_buffer(fetch_image(url)))
            )
            count += 1
        full_zip_in_memory = generate_zip(images_tuple)
        response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('images.zip')
        return response
    except :
        return HttpResponse(f"no image saved for requested date : {date}")
