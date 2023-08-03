from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from api.models import ReviveUser
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
# from .serializers import ReviveUserSerializer
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser,FormParser
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal,InvalidOperation
from rest_framework import generics
from datetime import datetime
from django.http import FileResponse


from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout,login
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404,redirect
from django.core import serializers

from django.http import JsonResponse
from api.models import ReviveUser
from .models import CrisisManage,EventManage,GalleryManage
from .serializers import CrisisManageSerializer,EventSerializer,GallerySerializer
# Create your views here.




class AdminLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print("Received from React:", email, password)
        
        try:
            user = ReviveUser.objects.get(email=email)
            
            print(user.is_admin,'this is super user status')
            password_check=check_password(password,user.password)
            print(password_check)
            if not password_check:
                print("incorrect password")
                return Response({'message': 'Password incorrect'})
            if user.is_admin is True or user.is_staff is True:
                login(request, user)
            
                print(request.user, 'this the user after login')
                print(user.is_admin,'this admin status')
                access_token = str(AccessToken.for_user(user))
                refresh_token = str(RefreshToken.for_user(user))
            
                return Response({
                    "message":'Success',
                    "user_id": user.id,
                    "staff_status":user.is_staff,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            return Response({'message': 'Unauthorized Login'})
        except ReviveUser.DoesNotExist:
            print("user does not exist")
            return Response({'message': 'There is no account Registerd with this Email'})
        



def userList_view(request):
    
    users = ReviveUser.objects.all()

    # Transform the fetched user data into a list of dictionaries
    user_data = []
    for user in users:
        user_data.append({
            'img': user.image.url,
            'volunteer': user.is_volunteer,
            'name': user.name,
            'email': user.email,
            'phone': [user.phone, user. marital_status],
            'online': user.is_active,
            
        })

    return JsonResponse(user_data, safe=False)

@csrf_exempt
@api_view(['POST'])
def user_block(request):
    email = request.data.get('email')
    print(email,'this axios email')
    user = ReviveUser.objects.get(email=email)
    print(user)
    if user is not None:
        print("inside 1 if")
        if user.is_active:
            print("inside 2 if")

            user.is_active = False
            print(user.is_active)
            user.save()
            return JsonResponse ({'message':'User blocked Successfully'})
        else :
            user.is_active = True
            user.save()
            return JsonResponse ({'message':'User Unblocked Successfully'})

    return JsonResponse ({'message':'Action Failed'})



def crisisList_view(request):

    datas = CrisisManage.objects.all()
    

    crisis_data = []
    for data in datas:
        
        crisis_data.append({
            'id':data.id,
            'img': data.image.url,
            'title': data.title,
            'description': data.description,
            'donation_goal': data.donation_goal,
            'recived_amount': data.recived_amount,
            # 'recived_amount': data.recived_amount,
            'is_active': data.is_active,

            
            
        })

    return JsonResponse(crisis_data, safe=False)



# class CrisisManageView(APIView):
#     def post(self, request, format=None):
#         print(request.data,"hhhhhhhhhhhhhhh")
#         serializer = CrisisManageSerializer(data=request.data)
#         print(serializer,"kkkkkkkkkkkkkkkkkkkk")
#         print(serializer.is_valid,'---------------------------------')
#         if serializer.is_valid():
#             print("but whyuuuuuuuuuuu")
#             serializer.save()
#             return Response({'message': 'Form data saved successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def crisis_adding(request):

    if request.method == 'POST':
        title= request.POST.get('title')
        donation_goal = request.POST.get('donation_goal')
        user_side = request.POST.get('user_side')
        user = ReviveUser.objects.get(id=user_side)
        print(user_side,'its from user side')
        if user:

            value= False
        else:
            value=True
        # isActive = value.lower() == 'true'

        description = request.POST.get('description')
        document = request.FILES.get('file')
        image = request.FILES.get('dropzone_file')
        print(image,'----------------------')
        print(document,'-----------------------')

        addcrisis = CrisisManage(user=user,title=title,donation_goal=donation_goal,is_active=value,description=description,
                                 document=document,image=image)
        addcrisis.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



    
@csrf_exempt
def crisis_update(request, crisis_id):
    if request.method == 'POST':
        # Retrieve the crisis object
        try:
            crisis = CrisisManage.objects.get(id=crisis_id)
        except CrisisManage.DoesNotExist:
            return JsonResponse({'error': 'Crisis not found'})
        title = request.POST.get('title')
        crisis.title = title
        crisis.donation_goal = request.POST.get('donation_goal')
        crisis.is_active = True 
        crisis.description = request.POST.get('description')
        
        file = request.FILES.get('file')
        image = request.FILES.get('dropzone_file')
        print(file)
        print(image)
        if image is not None:
            crisis.image = image

        else :
            pass
        if file is not None:
            crisis.document = file

        else :
            pass
            
        
            
        crisis.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

class CrisisDeleteView(APIView):
    def delete(self, request, id):
        crisis = CrisisManage.objects.filter(id=id).first()

        if not crisis:
            return Response({'message': 'Crisis not found'}, status=status.HTTP_404_NOT_FOUND)

        crisis.delete()
        return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)
    


class eventListCreateView(generics.ListCreateAPIView):
    queryset = EventManage.objects.all()
    serializer_class = EventSerializer

class EventUpdateView(APIView):
    def get_object(self, pk):
        try:
            return EventManage.objects.get(pk=pk)
        except EventManage.DoesNotExist:
            return None

    def put(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        print(request.data)
        # Check if the image data is present and not empty
         # Retrieve the date_time from request data
        date_time_str = request.data.get('date_time')
        date_time_str = request.data.get('date_time')

        # Check if date_time_str is not None and not empty
        if date_time_str:
            # Convert the date_time string to a Python datetime object
            # The input format of date_time_str should be: "YYYY-MM-DDTHH:MM"
            date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M")
            # Update the event's date_time field
            event.date_time = date_time_obj

        
        
        event.latitude = request.data.get('latitude')
        event.longitude = request.data.get('longitude')
        
        event.place = request.data.get('place')
        event.description = request.data.get('description')

        # Check if the image data is present and not empty
        image = request.data.get('image')
        print(image,'=====---------------')
        if image is not None and image == 'null':
            
            event.image = image
        else:
            pass

        # Save the updated event
        event.save()

        # Assuming you have a serializer for EventManage, you can serialize the updated event and return the response
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)




    def delete(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class galleryListCreateView(generics.ListCreateAPIView):
    queryset = GalleryManage.objects.all()
    serializer_class = GallerySerializer

class GalleryUpdateView(APIView):
    def get_object(self, pk):
        try:
            return GalleryManage.objects.get(pk=pk)
        except GalleryManage.DoesNotExist:
            return None

    def put(self, request, pk):
        gallery = self.get_object(pk)
        if not gallery:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        print(request.data)
   
        
        gallery.title = request.data.get('title')
        
        gallery.description = request.data.get('description')

        # Check if the image data is present and not empty
        image = request.data.get('image')
        if image is not None and image != 'null':
            gallery.image = image
        else:
            pass

        # Save the updated event
        gallery.save()

        
        serializer = GallerySerializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)




    def delete(self, request, pk):
        gallery = self.get_object(pk)
        if not gallery:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        gallery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','POST'])
def crisisApplication(request):

    if request.method == 'GET':
        crisis_applications = CrisisManage.objects.filter(is_active=False)

        crisis_data = []
        for data in crisis_applications:
        
            crisis_data.append({
                'id':data.id,
                'image': data.image.url,
                'user': data.user.name,
                'title': data.title,
                
                'is_active': data.is_active,
  
            })

        return JsonResponse(crisis_data, safe=False)
    
    elif request.method == 'POST':
        print("===========im in elif==========")
        crisis_id = request.data.get('CrisisId') 
        print(crisis_id,"===========its id==========")

        print(crisis_id,'---------------this is complint id--------')
        complaint = CrisisManage.objects.get(id=crisis_id)

        response = FileResponse(complaint.document)
        response['Content-Disposition'] = f'attachment; filename="{complaint.document.name}"'
        return response
    

@api_view(['GET','POST','PUT'])
def crisisApprovel(request,id):

    try:
        crisis_applications = CrisisManage.objects.get(id=id)
        crisis_applications.is_active = True
        crisis_applications.save()
        print("=======================upated=====================")
        return JsonResponse({'message':'success'}, safe=False)
    
    except:

        print("something failed")
        return JsonResponse({'message':'failed'}, safe=False)

    