from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from service_api.swagger import UsernameHeader
from service_api.utils import username_required


class UserDataView(HTTPMethodView):
    @doc.summary("Returns all users documents")
    @doc.consumes(UsernameHeader, location="header", required=True)
    @username_required()
    async def get(self, request: Request):
        collection = request.app.db[request.headers["username"]]
        docs = await collection.find().to_list(length=None)
        for document in docs:
            document['id'] = str(document['_id'])
            del document['_id']
        result = {
            "documents_count": docs
        }
        return json(result)

    @doc.summary("Add new document(s) to user collection")
    @doc.consumes(UsernameHeader, location="header", required=True)
    @doc.consumes(doc.JsonBody(description="Any json data to store"),
                  location="body", required=True)
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

        collection = request.app.db[request.headers["username"]]
        result = await collection.insert_one(request.json)
        return json({"status": "OK", "record_id": str(result.inserted_id)})

    @doc.summary("Delete document(s) from user collection")
    @doc.consumes(UsernameHeader, location="header", required=True)
    @doc.consumes(doc.JsonBody(
        description="Json for filtering data to delete"), location="body",
        required=True)
    @username_required()
    async def delete(self, request: Request):
        if not request.json:
            return json(
                {"error": "Provide json data!"},
                status=404
            )

        collection = request.app.db[request.headers["username"]]
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
