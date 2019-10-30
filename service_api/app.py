from sanic import Sanic
from motor.motor_asyncio import AsyncIOMotorClient
from sanic_openapi import swagger_blueprint

from service_api import config, api_v1

app = Sanic(__name__)
app.config.from_object(config)

api_v1.load_api(app)
app.blueprint(swagger_blueprint)


@app.listener('before_server_start')
def init(sanic: Sanic, loop):
    cfg = sanic.config
    sanic.db = AsyncIOMotorClient(cfg.DB_HOST, cfg.DB_PORT)[cfg.DB_NAME]
