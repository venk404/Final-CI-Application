from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from Models import insertstudent, get_all_students
from Models import get_student_by_Id, Update_student, delete_student
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Optional
from dotenv import load_dotenv
import os
import json


load_dotenv()


class Student(BaseModel):

    name: str = Field(examples=["Ganesh Gaitonde"])
    email: EmailStr = Field(examples=["Gopalmate@gmail.com"])
    age: int = Field(examples=[22])
    phone: str = Field(pattern=r'^\d{10}$', min_length=10, max_length=10,
                       examples=[1234567890])

    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            'examples': [
                {
                    "name": "Ganesh Gaitonde",
                    "email": "Gopalmate@gmail.com",
                    "age": 22,
                    "phone": "1234567890"
                }
            ]
        }
    )


class UpdateStudent(BaseModel):

    name: Optional[str] = Field(default=None, examples=["Ganesh Gaitonde"])
    email: Optional[EmailStr] = Field(default=None,
                                      examples=["Gopalmate@gmail.com"])
    age: Optional[int] = Field(default=None, examples=[22])
    phone: Optional[str] = Field(default=None, pattern=r'^\d{10}$',
                                 min_length=10,
                                 max_length=10, examples=[1234567890])

    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            'examples': [
                {
                    "name": "Ganesh Gaitonde",
                    "email": "Gopalmate@gmail.com",
                    "age": 22,
                    "phone": "1234567890"
                }
            ]
        }
    )


app = FastAPI()

version_v1 = APIRouter()
version_v2 = APIRouter()


# Custom handler for 422 Unprocessable Entity

@app.middleware("http")
async def handle_malformed_json(request: Request, call_next):
    """
    Middleware to catch malformed JSON in the request body.
    """
    if request.headers.get("content-type") == "application/json":
        try:
            await request.json()  # Try parsing the JSON body
        except json.JSONDecodeError as e:
            return JSONResponse(
                status_code=400,
                content={
                    "error": '''Given Json is not well
                            formetted, please check the input Json''',
                    "details": str(e),
                },
            )
    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")

    error_messages = []
    for error in exc.errors():
        loc = " -> ".join(str(i) for i in error["loc"])
        msg = error["msg"]
        type_error = error["type"]

        # Customize messages for specific field and error types
        if type_error == "value_error.number.not_a_number":
            msg = "The value provided is not a valid number. Check the input."
        elif type_error.startswith("type_error"):
            msg = f'''Invalid type for {loc}.
                    Expected a valid {type_error.split('.')[-1]}.'''

        error_messages.append(f"{loc}: {msg}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed for the input data.",
            "details": error_messages,
        },
    )


@version_v1.post("/AddStudent", status_code=200)
async def create_student(student: Student) -> Student:
    try:
        logger.info("Create student process Started...")
        res = jsonable_encoder(insertstudent(data=student))
        if res['status'] == "success":
            logger.info("Create student process Completed...")
            return JSONResponse(content={"message": "Student data added",
                                         "student_id": res["student_id"]})
        else:
            logger.error("Create student process InComplete...")
            raise HTTPException(status_code=400, detail=res['message'])
    except Exception as e:
        logger.error(f"Error while completing the get student process...{e}")
        return JSONResponse(status_code=400, content=e)


@version_v1.get("/GetAllStudents", status_code=200)
async def get_students() -> dict:
    try:
        logger.info("Get all student process Started...")
        res = jsonable_encoder(get_all_students())
        if res['status'] == "success":
            logger.info("Get all student process Completed...")
            return JSONResponse(content=res['students'])
        else:
            logger.error("Get all student process InComplete...")
            return JSONResponse(status_code=400,
                                content={"detail": res['message']})
    except Exception as e:
        logger.error(f'''Error while completing the get
                    all student process...{e}''')
        return JSONResponse(status_code=400, content=e)


@version_v1.get("/GetStudent", status_code=200)
async def get_student(id: int) -> dict:
    try:
        logger.info("Get student process Started...")
        res = get_student_by_Id(id)
        if res['status'] == "success":
            logger.info("Get student process Completed...")
            return JSONResponse(content=res['students'])
        else:
            logger.error("Get student process InComplete...")
            return JSONResponse(status_code=400,
                                content={"detail": res['message']})
    except Exception as e:
        logger.error(f"Error while completing the get student process...{e}")
        return JSONResponse(status_code=400, content=e)


@version_v2.patch("/UpdateStudent", status_code=200)
async def Update(id: int, student: UpdateStudent) -> dict:
    try:
        logger.info("Update student process Started...")
        res = Update_student(id, student)
        if res['status'] == "success":
            logger.info("Update student process Completed...")
            return JSONResponse(content={"message": res["message"]})
        else:
            logger.error("Update student process InComplete...")
            raise HTTPException(
                status_code=400,
                detail=res['message']
            )
    except Exception as e:
        logger.error(f'''Error while completing
                      the updating student process...{e}''')
        return JSONResponse(status_code=500, content={"detail": str(e)})


@version_v2.delete("/DeleteStudent", status_code=200)
async def delete(id: int) -> dict:
    try:
        logger.info("Delete student process Started...")
        res = delete_student(id)
        if res['status'] == "success":
            logger.info("Delte student process Completed...")
            return JSONResponse(content={"message": res["message"]})
        else:
            logger.error("Delte student process InComplete...")
            raise HTTPException(
                status_code=400,
                detail=res['message']
            )
    except Exception as e:
        logger.error(f'''Error while completing the
                      deleting student process...{e}''')
        return JSONResponse(status_code=500, content={"detail": str(e)})


@version_v1.get("/HealthCheck", status_code=200)
async def HealthCheck() -> dict:
    message = "All services is Up"
    return {"message": message}


app.include_router(version_v1, tags=['Version 1 Api Endpoints'])
app.include_router(version_v2, prefix='/v2', tags=['Version 2 Api Endpoints'])


if __name__ == "__main__":
    # Get the PORT from environment variable, or default to 8000
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
