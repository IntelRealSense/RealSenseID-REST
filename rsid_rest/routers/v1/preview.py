# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from loguru import logger
from starlette.responses import StreamingResponse

from rsid_rest.rsid_lib.rsid_api_wrapper import RSIDApiWrapper, get_rsid_api

router = APIRouter(
    prefix="/preview",
    tags=["preview"],
)


# Make sure that this function is not async in order to let FastAPI
# use `iterate_in_threadpool()`
# See: https://stackoverflow.com/a/75760884/4405028
@router.get(
    "/stream/",
    name="v1:preview:stream",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    responses={
        "422": {
            "description": "Unprocessable Entity - error while starting stream. "
                           "Possibly due to device issue, try again later.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"},
                }
            },
        },
    },
)
def stream(
    request: Request,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
) -> StreamingResponse:
    try:
        ticket: uuid.UUID = uuid.uuid4()

        # Further optimizations (aiortc?) :
        # https://github.com/tiangolo/fastapi/discussions/10104#discussioncomment-6785703

        response = StreamingResponse(
            api_wrapper.stream(ticket),
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            media_type="multipart/x-mixed-replace;boundary=frame",
        )
        return response

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
