from sanic import Sanic, Blueprint

from service_api.controllers.user_data import UserDataView


def load_api(app: Sanic):
    api_v1 = Blueprint("v1", url_prefix=None)

    api_v1.add_route(UserDataView.as_view(), "/")

    app.blueprint(api_v1)
