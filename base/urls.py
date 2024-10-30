
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('',views.home,name="home"),
    path('sector-pie/',views.sector_pie,name="sector_pie"),
    path('sector-pie-filter/',views.sector_pie_filter,name="sector_pie_filter"),
    path('pestle-bar/',views.pestle_bar,name="pestle_bar"),
    path('intensity-line/',views.intensity_line,name="intensity_line"),
    path('data-table/',views.data_table,name="data_table"),
    path('data-table-filter/',views.data_table_filter,name="data_table_filter"),

   
    #path('save_data/',views.save_data,name="save_data")
]
