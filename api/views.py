
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import ReviveUser,Department,Complaint,StaffApplication
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReviveUserSerializer,ReviveSerializer,DepartmentSerializer,ComplaintSerializer,StaffListSerializer
from rest_framework.request import Request
from rest_framework import generics
from django.http import FileResponse
from django.http import HttpResponse
from Admin.models import CrisisManage,EventManage,GalleryManage,Wallet
from Admin.serializers import CrisisManageSerializer

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

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret =  settings.STRIPE_WEBHOOK_SECRET

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL



@api_view(['POST'])
def SignupView(request):
        serializer = ReviveUserSerializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            user=serializer.save()
            send_verification_email(user)  # Send verification email to the user
            return Response(serializer.data)
        return Response({'error': 'Bad request'}, status=400)

def send_verification_email(user):
    subject = 'Verify your email'
    message = f'Hi {user.name},\n\nPlease click the following link to verify your email: http://127.0.0.1:8000/verify/{user.id}\n\nThanks!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])



@api_view(['GET'])
def email_verification(request, user_id):
    user = get_object_or_404(ReviveUser, id=user_id)
    
    if not user.is_active: 
        user.is_active = True
        user.save()
        print("user veryfied")
        return redirect('http://localhost:5173/login')
    print("user not veryfied")
    
    return Response({'message': 'Email already verified.'})


from rest_framework.exceptions import AuthenticationFailed

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print("Received from React:", email, password)
        
        try:
            user = ReviveUser.objects.get(email=email)
            print(user.password,'this is user model password')
            userpass=user.password
            print(user.is_superuser,'this is super user status')
            print("user", user,password)
            password_check=check_password(password,user.password)
            print(password_check)
            if not password_check:
                print("incorrect password")
                return Response({'message': 'Password incorrect'})
            
            login(request, user)
            
            print(request.user, 'this the user after login')
            print(user.is_admin,'this admin status')
            access_token = str(AccessToken.for_user(user))
            refresh_token = str(RefreshToken.for_user(user))
            
            return Response({
                "message":'Success',
                "user_id": user.id,
                
                "access_token": access_token,
                "refresh_token": refresh_token
            })
            
        except ReviveUser.DoesNotExist:
            print("user does not exist")
            return Response({'message': 'There is no account Registerd with this Email'})




class ComplaintRegisterView(APIView):
    def post(self, request):
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Complaint registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def logout_view(request):
    user=request.user
    print(user)
    logout(request)
    print(user,'after logoutt')

    return JsonResponse({'message': 'Logged out successfully!'})


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = ReviveUser.objects.all()
    serializer_class = ReviveSerializer
    lookup_field = 'id' 





# def user_data(request):
#     my_value = request.GET.get('user_id')
#     # print(request.user,my_value,'befote geting from context')
#     user = ReviveUser.objects.get(id=my_value)
#     print(user,'after geting from context')

#     data = {
#         'name':user.name,
#         'age':user.age,
#         'Martial_Status':user.marital_status,
#         'blood_group':user.blood_group,
#         'phone':user.phone,
#         'email': user.email,
#         'address': user.address,
#         'image':user.image
#     }
#     return JsonResponse(data)

@csrf_exempt
@api_view(['PUT'])
def update_user(request:Request, user_id):
    user = ReviveUser.objects.get(id=user_id)
    print(user,'this is the user')
    # data={
    #     # 'name':request.POST['name'],
    #     # 'email':request.POST['email'],
    #     'address':request.POST['address'],
    # }
    serializer = ReviveUserSerializer(user, data=request.data, partial=True)
    print(serializer,'this serilzer')
    if serializer.is_valid():
        user=serializer.save()
        
        print(serializer.errors)
        return JsonResponse({'message': 'User Updated Successfully'})
    return JsonResponse({'message': 'Updation failed'})


@api_view(['POST'])
def forgetPassword(request,email):

    
    print(email,'-----------------------------')
    user = ReviveUser.objects.get(email=email)
    subject = 'Verify your email'
    message = f'Hi {user.name},\n\nPlease click the following link to verify your email:http://localhost:5173/reset-pass/{user.id}\n\nThanks!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])
    

    return Response({"message":'mail send'})


class ChangePasswordView(APIView):
    def put(self, request, user_id):
        user = get_object_or_404(ReviveUser, id=user_id)
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Password field is required'}, status=status.HTTP_400_BAD_REQUEST)
    


def crisis_view(request,id):
    crisis = CrisisManage.objects.get(id=id)

    data = {
        'image' : crisis.image.url,
        'title' : crisis.title,
        'description' : crisis.description,
        'donation_goal': crisis.donation_goal,
        'recived_amount': crisis.recived_amount,
    }

    return JsonResponse(data)


class CrisisList(APIView):
    def get(self, request, format=None):
        crisis = CrisisManage.objects.filter(is_active=True)
        serializer = CrisisManageSerializer(crisis, many=True)
        return Response(serializer.data)


def download_file(request,id):
    print(id,'this is id from react -----------------------------------')
    crisis = CrisisManage.objects.get(id=id)
    file_data = crisis.document.read()  # Replace this with the actual file data from your backend
    filename = "CrisisProof.pdf"  # Replace this with the desired filename

    # Create an HTTP response with the file data and appropriate headers
    response = HttpResponse(file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response





def event_single(request,id):
    event = EventManage.objects.get(id=id)

    data = {
        'image' : event.image.url,
        'title' : event.title,
        'description' : event.description,
        'place': event.place,
        'date_time': event.Date_time,
        'lat':event.latitude,
        'lng':event.longitude
    }

    return JsonResponse(data)



class departmenttCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@csrf_exempt
def apply_for_staff(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email,'this the mail----------------------v-------------------')
        id_card = request.FILES.get('id_card')
        sector = request.POST.get('sector')

        try:
            user = ReviveUser.objects.get(email=email) 
            department = Department.objects.get(name=sector)
        

            # Save the staff application to the database
            staff_application = StaffApplication(user=user, department=department, id_card=id_card)
            staff_application.save()
        except:
            return JsonResponse({'error': 'Invalid request method'})

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@api_view(['GET'])
def staffApplication(request):

    if request.method == 'GET':
        staff_applications = StaffApplication.objects.all()

        staff_data = []
        for data in staff_applications:
        
            staff_data.append({
                'id':data.id,
                'image': data.user.image.url,
                'email': data.user.email,
                'department': data.department.name,
                'id_card': data.id_card.url,
                'is_aproved': data.is_approved,
                

                
                
            })

    return JsonResponse(staff_data, safe=False)



@api_view(['PUT'])
def staffApprovel(request,email):

    try:
        staff = ReviveUser.objects.get(email=email)
        application = StaffApplication.objects.get(user=staff)
        staff.is_staff = True
        staff.save()
        application.is_approved =True
        application.save()
        return JsonResponse({'message':'Success'})
    except:
        return JsonResponse({'message':'error occuerd'})





@api_view(['GET','POST'])
def complaintView(request):
    
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        # user = request.data.get('user_id')

        print(user_id,'------------------------Get-------------')
        # print(user,'------------------------Data-------------')

        if user_id :
            print("im in if-----------")
            complaints = Complaint.objects.filter(user=user_id)
            print(complaints,'---------=============--------==========')
            

        else:
            complaints = Complaint.objects.all()

        complaint_data = []
        for data in complaints:
        
            complaint_data.append({
                'id':data.id,
                'image': data.user.image.url,
                'name': data.name,
                'department': data.department.name,
                'document': data.document.url,
                'status': data.status,
                

                
                
            })

        return JsonResponse(complaint_data, safe=False)
    

    elif request.method == 'POST':
        print("===========im in elif==========")
        complaint_id = request.data.get('complaint_id') 
        print(complaint_id,"===========its id==========")

        print(complaint_id,'---------------this is complint id--------')
        complaint = Complaint.objects.get(id=complaint_id)

        response = FileResponse(complaint.document)
        response['Content-Disposition'] = f'attachment; filename="{complaint.document.name}"'
        return response
    



@api_view(['PUT'])
def complaintUpdate(request,id):
    complaint = Complaint.objects.get(id=id)
    print(complaint,'------------------------complaint------------------')
    status = request.data.get('status')
    print(status,'---------------------status------------------')

    if complaint:
        complaint.status=status
        complaint.save()
        print(complaint.status,'------------------this comlaint status-----------------')
        return Response({'message':'success'})
    else:
        return Response({'message':'error'})
    





class CreateCheckoutSession(APIView):
    def handle_successful_payment(self, crisis_id, amount):
        if crisis_id:

            print(amount,"------------im in price in saving---------------------------")
            # Update Crisis model with received amount
            price = int(amount/100)
            crisis = CrisisManage.objects.get(id=crisis_id)
            crisis.recived_amount += int(price)
            crisis.save()
        else:
            # Update Wallet model with received amount
            price = int(amount/100)
            wallet = Wallet.objects.first()  # Assuming there's only one wallet instance
            wallet.balance += int(price)
            wallet.save()

    def post(self, request):
        
        price = int(request.data.get('price')) * 100

        print(price,'------------this price-------after multiply----------------')
        crisis_id = request.data.get('crisis_id')

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                            'name': 'Product Name',  # Replace with actual product name
                        },
                        'unit_amount': price
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=FRONTEND_CHECKOUT_SUCCESS_URL,
                cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
            )


            # data={
            #     'url':checkout_session.url
            # }
            print(checkout_session.url,'------------------this is that url--------------------------')
            print(request.data)
            location = checkout_session.url
            print(location,'-------------------this locat-------------------')
            # Call handle_successful_payment after successful payment
            
            self.handle_successful_payment(crisis_id, price)

            # Redirect user to the checkout session URL
            return Response(location)
        except Exception as e:
            print(e)
            return Response({'message':'erroe'})

        
        

    


class WebHook(APIView):
  def post(self , request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
      event = stripe.Webhook.construct_event(
        payload ,sig_header , webhook_secret
        )
    except ValueError as err:
        # Invalid payload
        raise err
    except stripe.error.SignatureVerificationError as err:
        # Invalid signature
        raise err

    # Handle the event
    if event.type == 'payment_intent.succeeded':
      payment_intent = event.data.object 
      print("--------payment_intent ---------->" , payment_intent)
    elif event.type == 'payment_method.attached':
      payment_method = event.data.object 
      print("--------payment_method ---------->" , payment_method)
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event.type))

    return JsonResponse(success=True, safe=False)
    



@api_view(["PATCH"])
def become_volunteer(request, user_id):
    try:
        print("we are in try volunteer")
        user = ReviveUser.objects.get(id=user_id)
        user.is_volunteer = True
        user.save()
        return Response(status=status.HTTP_200_OK)
    except ReviveUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
                
