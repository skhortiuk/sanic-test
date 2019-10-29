from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from motor.motor_asyncio import AsyncIOMotorClient

import config
from utils import username_required

app = Sanic(__name__)
app.config.from_object(config)


@app.middleware('response')
async def ensure_headers(request, response):
    response.headers["content-type"] = "application/json"


@app.listener('before_server_start')
def init(sanic: Sanic, loop):
    cfg = sanic.config
    sanic.db = AsyncIOMotorClient(cfg.DB_HOST, cfg.DB_PORT)[cfg.DB_NAME]


class UserDataListView(HTTPMethodView):
    @username_required()
    async def get(self, request: Request):
        collection = app.db[request.headers["username"]]
        docs = await collection.find().to_list(length=None)
        for doc in docs:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        result = {
            "documents_count": docs
        }
        return json(result)

    @username_required()
    async def post(self, request: Request):
        if not request.json:
            return json(
                {
                    "status": "ERROR",
                    "error_code": 404,
                    "error": "Provide json data!",
                },
                status=404
            )

        collection = app.db[request.headers["username"]]
        result = await collection.insert_one(request.json)
        return json({"status": "OK", "record_id": str(result.inserted_id)})

    @username_required()
    async def delete(self, request: Request):
        if not request.json:
            return json(
                {"error": "Provide json data!"},
                status=404
            )

        collection = app.db[request.headers["username"]]
        documents_count = await collection.count_documents(request.json)
        if documents_count < 1:
            return json(
                {
                    "status": "ERROR",
                    "error_code": 404,
                    "error": "No data found!"
                },
                status=404
            )

        deleted = await collection.delete_many(request.json)

        return json(
            {
                "status": "OK",
                "deleted_count": deleted.deleted_count
            },
            status=200
        )


app.add_route(UserDataListView.as_view(), "/")

if __name__ == '__main__':
    app.run("0.0.0.0", port=8008)
