from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from shareRes.models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
import urllib.request
from code import * 

# Create your views here.

def sendEmail(request):
    checked_res_list = request.POST.getlist('checks')
    inputRecevier = request.POST['inputReceiver']
    inputTitle = request.POST['inputTitle']
    inputContent = request.POST['inputContent']
    
    mail_html = "<html><body>"
    mail_html += "<h1> 맛집 공유 </h1>"
    mail_html += "<p>"+inputContent+"<br>"
    mail_html += "발신자님께서 공유하신 맛집은 다음과 같습니다.</p>"
    for checked_res_id in chcked_res_list:
        restaurant = Restaurant.objects.get(id = checked_res_id)
        mail_html += "<h2>"+restaurant.restaurant_name+"</h3>"
        mail_html += "<h4>* 관련 링크</h4>"+"<p>"+restaurant.restaurant_link+"</p><br>"
        mail_html += "<h4>* 관련 키워드</h4>"+"<p>"+restaurant.restaurant_keyword+"</p><br>"
        mail_html += "<br>"
    mail_html +="</body></html>"
    # print(checked_res_list,"/",inputReceiver,"/",inputTitle,"/",inputContent)
    # print(mail_html)
    # stmp using
    server = smtp.SMTP_SSL('smtp.gmail.com',465)
    server.login("arcipond@gmail.com","kidaexqrbsmqjsyb")
    
    msg - MIMEMultipart('alternative')
    msg['Subject'] = inputTitle
    msg['From'] = 'arcipond@gmail.com'
    msg['To'] = inputReceiver
    mail_html = MIMEText(mail_html, 'html')
    msg.attach(mail_html)
    print(msg['To'], type(msg['To']))
    server.sendmail(msg['From'],msg['To'].split(','),msg.as_string())
    server.quit()
    return HttpResponseRedirect(reverse('index'))
    # return HttpResponse("sendEmail")
    
def index(request):
    #return HttpResponse('<h1> hello </h1>')
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()
    content = {'categories': categories, 'restaurants':restaurants}  
    return render(request, 'shareRes/index.html', content)

def restaurantDetail(request,res_id):
    restaurant = Restaurant.objects.get(id = res_id)
    content = {'restaurant' : restaurant}
    return render(request, 'shareRes/restaurantDetail.html', content)


def restaurantCreate(request):
    categories = Category.objects.all()
    content = {'categories':categories}
    return render(request, 'shareRes/restaurantCreate.html', content)

def restaurantUpdate(request,res_id):
    categories = Category.objects.all()
    restaurant = Restaurant.objects.get(id = res_id)
    content = {'categories': categories, 'restaurant':restaurant}
    return render(request, 'shareRes/restaurantUpdate.html', content)

def Delete_restaurant(request):    
    res_id = request.POST['resId']
    restaurant = Restaurant.objects.get(id = res_id)
    restaurant.delete()
    return HttpResponseRedirect(reverse('index'))

def Update_restaurant(request):
    resId = request.POST['resId']
    change_category_id = request.POST['resCategory']
    change_category = Category.objects.get(id = change_category_id)
    change_name = request.POST['resTitle']
    change_link = request.POST['resLink']
    change_content = request.POST['resContent']
    change_keyword = request.POST['resLoc']
    before_restaurant = Restaurant.objects.get(id = resId)
    before_restaurant.category =change_category
    before_restaurant.restaurant_name = change_name
    before_restaurant.restaurant_link = change_link
    before_restaurant.restaurant_content = change_content
    before_restaurant.restaurant_keyword = change_keyword
    before_restaurant.save()
    return HttpResponseRedirect(reverse('resDetailPage', kwargs={'res_id':resId}))

def Create_restaurant(request):
    category_id = request.POST['resCategory']
    category = Category.objects.get(id = category_id)
    name = request.POST['resTitle']
    link = request.POST['resLink']
    content = request.POST['resContent']
    keyword = request.POST['resLoc']
    new_res = Restaurant(category=category, restaurant_name=name, restaurant_link=link, restaurant_content=content, restaurant_keyword=keyword)
    new_res.save()
    return HttpResponseRedirect(reverse('index'))

def categoryCreate(request):
    categories = Category.objects.all()
    content = {'categories':categories}
    return render(request, 'shareRes/categoryCreate.html', content)

def Create_category(request):
    category_name = request.POST['categoryName']
    new_category = Category(category_name = category_name)
    new_category.save()
    return HttpResponseRedirect(reverse('index'))

def Delete_category(request):
    category_id = request.POST['categoryId']
    delete_category = Category.objects.get(id = category_id)
    delete_category.delete()
    return HttpResponseRedirect(reverse('cateCreatePage'))

def Book_sc(request):
    client_id = client_id123
    client_secret = client_secret123
    
    encText = urllib.parse.quote(request.GET["bookname"])
    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        b=response_body.decode('utf-8')
        return HttpResponse(b[2])
    else:
        return HttpResponse("Bad")