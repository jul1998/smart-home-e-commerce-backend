from .user import signup, login, hello_protected, logout, get_user_by_id, get_carritoCompras, change_password, display_settings, delete_account_by_id
from .product import create_product, get_product_list, add_to_favorite_list, get_favorite_product, get_product_info_by_id, add_product_description 
from .historial_compras import get_order_history
from .producto_preguntas import post_product_question, get_questions, delete_question_by_id
from .userAdmin import signupAdmin, loginAdmin
from .email_server import send_email
  