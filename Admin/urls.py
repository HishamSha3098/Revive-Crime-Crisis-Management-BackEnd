from django.urls import path
from .import views

urlpatterns = [
    # path('signup/', views.signup,name='signup'),
   
    path('adminLogin/', views.AdminLogin.as_view(),name='admin'),
    path('user_list/', views.userList_view,name='user_list'),
    path('crisis_list/', views.crisisList_view,name='crisis_list'),
    path('crisis_applications/', views.crisisApplication,name='crisis_applications'),
    path('crisis-approvel/<int:id>/', views.crisisApprovel,name='crisis-approvel'),
    path('user_manage/', views.user_block,name='user_manage'),
    # path('add_crisis/', views.CrisisManageView.as_view(), name='add_crisis'),
    path('add_crisis/', views.crisis_adding,name='add_crisis'),
    path('update_crisis/<int:crisis_id>/', views.crisis_update,name='update_crisis'),
    path('delete_crisis/<int:id>/', views.CrisisDeleteView.as_view(),name='delete_crisis'),
    # path('update_crisis/<int:pk>/', views.CrisisUpdate.as_view(),name='update_crisis'),
    # path('add_crisis/', views.CrisisCreate.as_view(), name='create_crisis'),

    path('event/', views.eventListCreateView.as_view(), name='event-list-create'),
    path('eventManage/<int:pk>/', views.EventUpdateView.as_view(), name='event-retrieve-update-destroy'),

    path('gallery/', views.galleryListCreateView.as_view(), name='gallery-list-create'),
    path('galleryManage/<int:pk>/', views.GalleryUpdateView.as_view(), name='gallery-retrieve-update-destroy'),

    

]
