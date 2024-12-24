import uvicorn
import logging
import dash
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from Callbacks import *
from Routing import set_routes
from fastapi.security import HTTPBearer
from constants import log_key
log_level = logging.DEBUG if False else logging.ERROR
logging.basicConfig(level=log_level)
logger = logging.getLogger(log_key)

app = FastAPI()
security= HTTPBearer()


def run():
    app.add_middleware(SessionMiddleware, secret_key="!secret")
    print("oauth")
    set_routes(app)
    return app



if __name__ == '__main__':
    uvicorn.run("main_app:run", host="0.0.0.0", port=5096, reload=True, factory=True, timeout_keep_alive=200,
                #debug=True
                )