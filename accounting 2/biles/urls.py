from django.urls import path
from  . import views


urlpatterns = [
    path('product/Ham/add/', views.addProductHam, name='addProductham'),
    path('Product/Ham/', views.ProductHam_List, name='ProductHam_List'),
    path('Product/Ham/<int:id>/', views.fatch_ProductHam, name='fatch_ProductHam'),
    path('Product/Ham/edit/<int:id>/', views.update_ProductHam, name='update_ProductHam'),
    path('Product/Ham/delete/<int:id>/', views.delete_ProductHamm, name='delete_ProductHamm'),
    path('Product/Ham/uplode/', views.uplode_ProductHam, name='uplode_ProductHam'),
    path('Product/ham/download/',views.download_ProductHam_csv, name='download_ProductHam_csv'),

    #end of  Product Ham

     path('pakage/add/', views.addPakage, name='addPakage'),
    path('pakage/', views.pakage_List, name='pakage_List'),
    path('pakage/<int:id>/', views.fatch_pakage, name='fatch_pakage'),
   path('pakage/edit/<int:id>/', views.update_pakage, name='update_pakage'),
    path('pakage/delete/<int:id>/', views.delete_pakage, name='delete_pakage'),
    path('pakage/uplode/', views.uplode_package, name='uplode_package'),
    path('pakage/download/',views.download_pakage_csv, name='download_pakage_csv'),
  #end of  project
    path('jar/add/', views.addjar, name='addjar'),
   path('jar/', views.jar_List, name='jar_List'),
    path('jar/<int:id>/', views.fatch_jar, name='fatch_jar'),
   path('jar/edit/<int:id>/', views.update_jar, name='update_jar'),
    path('jar/delete/<int:id>/', views.delete_jar, name='delete_jar'),
   path('jar/uplode/', views.uplode_jar, name='uplode_jar'),
    path('jar/download/',views.download_jar_csv, name='download_jar_csv'),


    #end of  jar

    path('product/add/', views.addProduct, name='addProduct'),
    path('product/', views.Product_List, name='Product_List'),
    path('product/<int:id>/', views.fatch_Product, name='fatch_Product'),
    path('Product/edit/<int:id>/', views.update_Product, name='update_Product'),
    path('Product/delete/<int:id>/', views.delete_Product, name='delete_Product'),
    path('Product/uplode/', views.uplode_product, name='uplode_product'),
    path('Product/download/',views.download_product_csv, name='download_Product_csv'),



  path('costomers/add', views.add_costomer, name='add_costomer'),
   path('costomers/', views.costomers_List, name='costomers_List'),
     path('costomers/<int:id>/', views.fatch_costomers, name='fatch_costomers'),
      path('costomers/edit/<int:id>/', views.update_costomers, name='update_costomers'),
     path('costomers/delete/<int:id>/', views.delete_costomers, name='delete_costomers'),
      path('costomers/uplode/', views.upload_customers, name='uplode_costomers'),
      path('costomers/download/',views.download_costomers_csv, name='download_costomers_csv'), #upload_uds_bills



  #      path('add/', views.addProduct, name='addProduct'),
 #   path('', views.Product_List, name='Product_List'),
    path('<int:id>/', views.view_bill, name='view_bills'),
  #  path('edit/<int:id>/', views.update_Product, name='update_Product'),
 #   path('delete/<int:id>/', views.delete_Product, name='delete_Product'),
    path('uplode/', views.upload_uds_bills, name='upload_uds_bills'),
   # path('download/',views.download_product_csv, name='download_Product_csv'),



  #      path('add/', views.addProduct, name='addProduct'),
   path('', views.fetch_bills_list_usd, name='fetch_bills_list_usd'),
 #   path('<int:id>/', views.fatch_Product, name='fatch_Product'),
  #  path('edit/<int:id>/', views.update_Product, name='update_Product'),
 #   path('delete/<int:id>/', views.delete_Product, name='delete_Product'),
    path('usd/inner/uplode/', views.upload_uds_bills_inner, name='upload_uds_bills_inner'),
   # path('download/',views.download_product_csv, name='download_Product_csv'),






#upload_uds_bill_inner

]



