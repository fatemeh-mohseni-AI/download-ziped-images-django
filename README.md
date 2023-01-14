# download-ziped-images-django
how to make url which download images from specific folder in a zip file

مسئله چیه :
می خواهیم تعدادی عکس رو به صورت یک فایل زیپ دانلود کنیم 
در واقع تصور کنید هرروز یک سری عکس توی ادرس زیر ذخیره میشه و ما میخوایم تمام عکس های یک دایرکتوری رو دانلود کنیم

                                                                                                         /media/pic/{date}/

در واقع اخرین دایرکتوری تاریخ روزی هست که عکسا داخلش سیو شدن
پس اگه همچین ادرسی تو کد ها دیدید بدونین جریان چیه .

------------------------------------------------------------------------------------------------------------------------------------------
image_list()

این تابع لیستی اس اسم عکس هایی که داخل دایرکتوری مشخصی هستند بهمون میده . و تو عملیات دانلود نیست . صرفا یه تابعه که نوشته بودم و گذاشتم تو فایل بمونه و اپلود کردم همین

fetch_image()

ادرس یک عکس رو میگیره و یک PIL IMAGE برمیگردونه

get_image_buffer()

تصویر PIL رو به عنوان آرگومان می گیره و تصویر رو در بافر ذخیره می کنه و تصویر بافر رو برمی گردونه

generate_zip()

از اسمش پیداس چیکار میکنه

download_to_zip()

تک تک عکس ها رو میفرسته تا فرایند بالا رو طی کنن و در اخر در HttpResponse فایل زیپ رو attach میکنه


------------------------------------------------------------------------------------------------------------------------------------------------------
اگر لازم بود تا عکس ها رو از نت دریافت کنید به جای اینکه جایی در دایرکتوری محلی ذخیره شده باشن باید از توابع زیر استفاده کنید

```
def fetch_image(url):
    ''' function to return pil image'''
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img
```
    
    
و زمانی که لیست ادرس عکس ها رو iterate میکنه باید ادرس کامل عکس رو در لیست ذخیره کرده باشین پس تابع زیر هم به این شکل میشه 

```
def download_to_zip(request):
    images_tuple = []
    images = [
        'https://wsvincent.com/assets/images/books/dfp_31.jpg',
        'https://pictures.abebooks.com/isbn/9781449367817-us.jpg',
        'https://djangostars.com/blog/uploads/2017/04/Python-Django-Books-Tutorials-For-Beginners.png',
        'https://images.milanuncios.com/api/v1/ma-ad-media-pro/images/296b1d59-04bf-46e4-a449-6815a222dbf5?rule=hw545',
        'https://lets-code-more.s3.amazonaws.com/static/assets/imgs/theme/COMPUTER.jpg'
    ]
    count = 0
    for i in images:
        images_tuple.append(
            ("image" + str(count) + ".jpg", get_image_buffer(fetch_image(i)))
        )
        count += 1
    full_zip_in_memory = generate_zip(images_tuple)
    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format('images.zip')
    return response
```











