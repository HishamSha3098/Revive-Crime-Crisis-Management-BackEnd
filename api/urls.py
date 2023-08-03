from django.urls import path
from .import views

urlpatterns = [
    # path('signup/', views.signup,name='signup'),
    path('signup/', views.SignupView,name='signup'),
    path('login/', views.UserLogin.as_view(),name='login'),
    # path('adminLogin/', views.AdminLogin.as_view(),name='admin'),
    path('logout/', views.logout_view, name='logout'),
    # path('user_data/', views.user_data, name='user_data'),
    path('user_data/<int:id>/', views.UserRetrieveView.as_view(), name='user-detail'),
    path('verify/<int:user_id>/', views.email_verification, name='email_verification'),
    path('updateuser/<int:user_id>/', views.update_user, name='update_user'),
    path('reset-password/<str:email>/', views.forgetPassword, name='resetPass'),
    path('passwordChange/<int:user_id>/', views.ChangePasswordView.as_view(), name='passwordChange'),

    path('Crisis-single/<int:id>/', views.crisis_view, name='crisisSingle'),
    path('crisis_list/', views.CrisisList.as_view(), name='crisis-list'),
    path('fileDownload/<int:id>/', views.download_file, name='fileDownload'),
    path('Event-single/<int:id>/', views.event_single, name='eventSingle'),

    path('department/', views.departmenttCreateView.as_view(), name='department'),
    path('Staff-apply/', views.apply_for_staff, name='Staff-apply'),

    path('staff-application/', views.staffApplication, name='staff-application'),
    path('make-staff/<str:email>', views.staffApprovel, name='make-staff'),
    path('complaints/', views.complaintView, name='complaints'),
    # path('complaints/<int:id>/', views.complaintView, name='complaints'),
    path('complaint/<int:id>/', views.complaintUpdate, name='complaint-status-update'),

    path('register_complaint/', views.ComplaintRegisterView.as_view(), name='register_complaint'),

    path('create-checkout-session/' , views.CreateCheckoutSession.as_view()),  
    path('webhook-test/' , views.WebHook.as_view()), 




]
