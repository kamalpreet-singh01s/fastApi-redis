from fastapi import APIRouter

from config import redis_db_obj
from schemas import Response, RequestBook

router = APIRouter()


# Get request for fetch all data
@router.get("/{key}")
async def get_data(key: str):
    _data = redis_db_obj.json().get(key, '$')
    if _data:
        message = "All data received successfully"
    else:
        message = "No data found"
    return Response(status="Ok",
                    code="200",
                    message=message,
                    result=_data)


# Post request for enter new data
@router.post("/create/{key}")
async def create_data(request: RequestBook, key: str):
    redis_db_obj.json().set(key, '$', dict(request.parameter))
    return Response(status="Ok",
                    code="200",
                    message="New data added successfully").dict(exclude_none=True)


# Patch request for update existing data
@router.patch("/update/{key}")
async def update_data(request: RequestBook, key: str):
    search_key = redis_db_obj.json().get(key, '$')
    if search_key:
        redis_db_obj.json().set(key, '$..id', request.parameter.id)
        redis_db_obj.json().set(key, '$..title', request.parameter.title)
        redis_db_obj.json().set(key, '$..description', request.parameter.description)

        return Response(status="Ok",
                        code="200",
                        message="The data has been successfully updated")
    else:
        return Response(
            status="Bad Request",
            code="400",
            message="Data not found"
        )


# Delete request fro delete existing data
@router.delete("/delete/{key}")
async def delete_data(key: str):
    search_key = redis_db_obj.json().get(key, '$')
    if search_key:
        redis_db_obj.json().delete(key, '$')
        return Response(status="Ok",
                        code="200",
                        message="The data has been successfully deleted").dict(exclude_none=True)
    else:
        return Response(status="Bad Request",
                        code="400",
                        message="Data not found").dict(exclude_none=True)
