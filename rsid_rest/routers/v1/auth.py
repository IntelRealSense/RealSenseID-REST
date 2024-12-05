# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger

from rsid_rest.core.config import get_app_settings
from rsid_rest.core.settings.base import ApplicationDBTypes
from rsid_rest.rsid_lib.gen.models import AuthenticateStatusEnum
from rsid_rest.rsid_lib.models import (
    AuthenticationResponse,
)
from rsid_rest.rsid_lib.rsid_api_wrapper import RSIDApiWrapper, get_rsid_api

router = APIRouter(
    prefix="/auth",
    tags=["users", "auth"],
)


@router.get(
    "/",
    name="v1:auth",
    responses={
        "406": {
            "description": "Authentication failure. Possibly due to face pose or other "
                           "issues. `status` will be set to the value of the possible error.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/AuthenticationResponse"},
                }
            },
        },
        "422": {
            "description": "Unprocessable Entity - exception during user enrollment. "
                           "Possibly due to device issue, try again later.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"},
                }
            },
        },
    },
)
async def auth(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
) -> AuthenticationResponse:
    try:
        result: AuthenticationResponse
        if get_app_settings().db_mode == ApplicationDBTypes.device:
            result = await api_wrapper.auth()
        else:
            result = await api_wrapper.auth_host()
        response.status_code = status.HTTP_200_OK
        if result.status != AuthenticateStatusEnum.Success:
            result.user_id = None  # Ensure we pass null instead of empty string
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return result
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
