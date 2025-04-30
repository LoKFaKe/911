shop_bp = Blueprint('shop', __name__)
@shop_bp.route('/')
def shop_index():
    return "Shop Microservice"
