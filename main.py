from fastapi import FastAPI
from fastapi.responses import JSONResponse
from route import *

app = FastAPI(
    title = "Global Terrorism Database API", default_response_class=JSONResponse
)

app.include_router(router)