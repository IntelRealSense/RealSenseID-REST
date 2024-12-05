# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from fastapi.responses import UJSONResponse
from loguru import logger
from pydantic import ValidationError


async def unhandled_exception_handler(_: Request, exc: HTTPException) -> UJSONResponse:
    return UJSONResponse(
        {"errors": [exc.detail]},
        status_code=exc.status_code,
        headers={"X-Request-ID": correlation_id.get() or ""},
    )


async def http422_error_handler(
    _: Request,
    exc: RequestValidationError | ValidationError,
) -> UJSONResponse:
    logger.error(jsonable_encoder(exc.errors()))
    return UJSONResponse(
        {"errors": jsonable_encoder(exc.errors())},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        headers={"X-Request-ID": correlation_id.get() or ""},
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": f"{REF_PREFIX}ValidationError"},
    },
}
