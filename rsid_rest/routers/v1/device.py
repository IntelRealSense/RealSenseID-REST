# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger

from rsid_rest.rsid_lib.gen.models import StatusEnum
from rsid_rest.rsid_lib.models import (
    DeviceConfig as DeviceConfigModel,
)
from rsid_rest.rsid_lib.models import (
    DeviceConfigResponse,
    DeviceInfoResponse,
)
from rsid_rest.rsid_lib.rsid_api_wrapper import RSIDApiWrapper, get_rsid_api

router = APIRouter(
    prefix="/device",
    tags=["device"],
)


@router.get(
    "/device-config/",
    name="v1:device:get-device-config",
    summary="Retrieve device configuration.",
    description="Retrieves device configuration. "
                "This method allows you to read the current settings of the device.\n\n",
    responses={
        "422": {
            "description": "Unprocessable Entity - exception during reading device configuration. "
                           "Possibly due to device issue, try again later.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"},
                }
            },
        }
    },
)
def query_device_config(
    response: Response, api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)]
) -> DeviceConfigResponse:
    try:
        device_config = api_wrapper.query_device_config()
        response.status_code = status.HTTP_200_OK

        return DeviceConfigResponse(config=device_config, status=StatusEnum.Ok)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.get(
    "/device-info/",
    name="v1:device:get-device-info",
    summary="Retrieve device info.",
    description="Retrieves device info. " "This method allows you to read the current in of the device.\n\n",
    responses={
        "422": {
            "description": "Unprocessable Entity - exception during reading device configuration. "
                           "Possibly due to device issue, try again later.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"},
                }
            },
        }
    },
)
def query_device_info(
    response: Response, api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)]
) -> DeviceInfoResponse:
    try:
        device_info = api_wrapper.query_device_info()
        response.status_code = status.HTTP_200_OK
        return device_info
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.put(
    "/device-config/",
    name="v1:device:put-device-config",
    summary="Update device configuration.",
    description="Update device configuration. "
                "This method allows you to update the current settings of the device.\n\n",
    responses={
        "422": {
            "description": "Unprocessable Entity - exception during reading device configuration. "
                           "Possibly due to device issue, try again later.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"},
                }
            },
        }
    },
)
def update_device_config(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
    config: Annotated[DeviceConfigModel, "DeviceConfig"],
) -> DeviceConfigResponse:
    try:
        device_config: DeviceConfigModel = api_wrapper.update_device_config(config)
        response.status_code = status.HTTP_200_OK

        return DeviceConfigResponse(config=device_config, status=StatusEnum.Ok)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
