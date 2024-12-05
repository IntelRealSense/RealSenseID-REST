# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from contextlib import asynccontextmanager
from pathlib import Path

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.gzip import GZipMiddleware # TODO
from fastapi.responses import FileResponse

from rsid_rest.core.config import get_app_settings
from rsid_rest.core.exception import http422_error_handler, unhandled_exception_handler
from rsid_rest.frontend import demo
from rsid_rest.routers.v1.auth import router as auth_router
from rsid_rest.routers.v1.device import router as device_router
from rsid_rest.routers.v1.preview import router as preview_router
from rsid_rest.routers.v1.users import router as users_router
from rsid_rest.routers.v1.utility import router as utility_router


@asynccontextmanager
async def lifespan(
    # pylint: disable=unused-argument
    application: FastAPI,
):
    yield


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    args = settings.fastapi_kwargs
    args["lifespan"] = lifespan
    application = FastAPI(**args)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # TODO: Add this back after we remove it from the preview stream
    # application.add_middleware(GZipMiddleware, minimum_size=1000)
    application.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
        update_request_header=True,
    )

    application.add_exception_handler(HTTPException, unhandled_exception_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(router=users_router, prefix=settings.api_v1_prefix)
    application.include_router(router=device_router, prefix=settings.api_v1_prefix)
    application.include_router(router=auth_router, prefix=settings.api_v1_prefix)
    application.include_router(router=preview_router, prefix=settings.api_v1_prefix)
    application.include_router(router=utility_router, prefix=settings.api_v1_prefix)

    return application


app = get_application()


# # Load balancer health-check will ping this route very frequently. Let's make it as light as possible.
# @app.get("/", name="app:root")
# async def root():
#     data = b'{"message": "VisionPlatform/RSID Applications."}'
#     return Response(content=data, media_type="application/json")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = Path(__file__).resolve().parents[0] / "favicon.ico"
    if Path(favicon_path).exists():
        return FileResponse(favicon_path)
    else:
        raise HTTPException(status_code=404, detail="")


demo.init(app)
