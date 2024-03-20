Первое задание содержится в файле task_1
Второе задание включает в себя проект на django - task_2 и приложение products
Для перехода в админку можно воспользоваться суперюзером 
{
  "username": "admin",
  "password": "admin"
}

Для авторизации http://127.0.0.1:8000/create/ методом POST
{
  "username": "...",
  "password": "..."
}

Для получения токена http://127.0.0.1:8000/login/  методом POST
{
  "username": "...",
  "password": "..."
}

Вставляем токен в Authorization и получаем доступ к вот этим вьюшкам
    path('users/<int:user_id>/add-product/<int:product_id>/<int:quantity>/', UserCartViewSet.as_view({'post': 'add_or_create_product_to_cart'})),
    path('users/<int:user_id>/remove-product/<int:product_id>/', UserCartViewSet.as_view({'delete': 'remove_product_from_cart'})),
    path('users/<int:user_id>/cart/', UserCartViewSet.as_view({'get': 'get_cart_contents'})),
    path('users/<int:user_id>/clear-cart/', UserCartViewSet.as_view({'delete': 'clear_cart'})),
