# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import tempfile
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)
from loguru import logger

from rsid_rest.core.config import get_app_settings
from rsid_rest.core.settings.base import ApplicationDBTypes
from rsid_rest.rsid_lib.gen.models import EnrollStatusEnum, StatusEnum
from rsid_rest.rsid_lib.models import (
    CommonOperationResponse,
    EnrollResponse,
    UsersQueryResponse,
)
from rsid_rest.rsid_lib.rsid_api_wrapper import RSIDApiWrapper, get_rsid_api

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

status_error_links = {
    "status": {
        "description": "The `status` value returned in the response can be used either of the following:",
    }
}


@router.post(
    "/enroll/",
    name="v1:users:enroll",
    summary="Enroll a user with `user_id` in device database",
    status_code=201,
    responses={
        "406": {
            "description": "Enrollment failure. Possibly due to face pose or other issues. `status` will be set "
                           "to the cause of the failure.\n",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/EnrollResponse"},
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
async def enroll(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
    user_id: Annotated[str, Query(max_length=100, min_length=1)],
) -> EnrollResponse:
    try:
        result: EnrollResponse
        if get_app_settings().db_mode == ApplicationDBTypes.device:
            result = await api_wrapper.enroll(user_id=user_id)
        else:
            result = await api_wrapper.enroll_host(user_id=user_id)
        response.status_code = status.HTTP_201_CREATED

        if result.status != EnrollStatusEnum.Success:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return result
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.post(
    "/enroll-image/",
    name="v1:users:enroll-images",
    summary="Enroll a user with `user_id` in device database using image",
    status_code=201,
    responses={
        "406": {
            "description": "Enrollment failure. Possibly due to face pose or other issues. `status` will be set "
                           "to the cause of the failure.\n\n",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/EnrollResponse"},
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
async def enroll_image(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
    user_id: Annotated[str, Query(max_length=100, min_length=1)],
    background_tasks: BackgroundTasks,
    file: Annotated[
        UploadFile,
        File(
            title="Enroll Image",
            description="Photo of user to enroll",
            alias="EnrollImageFileUpload",
            alias_priority=1,
        ),
    ],
) -> EnrollResponse:
    async def delete_temp_uploads(uploaded_file: Path | None) -> None:
        if uploaded_file is not None and uploaded_file.exists():
            try:
                logger.info(f"Deleting temporary file {uploaded_file.name}")
                uploaded_file.unlink(missing_ok=True)
            except OSError as os_e:
                logger.error(os_e)

    temp_path: Path | None = None
    try:
        temp_path = Path(tempfile.gettempdir()) / file.filename
        async with aiofiles.open(temp_path, "wb") as f:
            while chunk := await file.read(size=1024 * 1024):
                await f.write(chunk)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading file",
        ) from e
    finally:
        await file.close()

    try:
        result: EnrollResponse
        if get_app_settings().db_mode == ApplicationDBTypes.device:
            result = await api_wrapper.enroll_image(user_id=user_id, file_path=temp_path)
        else:
            result = await api_wrapper.enroll_host_image(user_id=user_id, file_path=temp_path)
        response.status_code = status.HTTP_201_CREATED

        if result.status != EnrollStatusEnum.Success:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        # nicegui doesn't like background_tasks?
        background_tasks.add_task(delete_temp_uploads, uploaded_file=temp_path)

        return result
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.get(
    "/",
    name="v1:users:users",
    summary="Get all users",
    responses={
        "422": {
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"},
                }
            },
        }
    },
)
async def query_users(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)]
) -> UsersQueryResponse:
    try:
        users: list[str]
        if get_app_settings().db_mode == ApplicationDBTypes.device:
            users = await api_wrapper.query_users()
        else:
            users = await api_wrapper.query_host_users()
        response.status_code = status.HTTP_200_OK
        return UsersQueryResponse(users=users)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.delete("/clear-all/", name="v1:users:remove_all_users")
def remove_all_users(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)]
) -> CommonOperationResponse:
    try:
        if get_app_settings().db_mode == ApplicationDBTypes.device:
            api_wrapper.remove_all_users()
        else:
            raise RuntimeError("Not implemented.")
        response.status_code = status.HTTP_200_OK
        return CommonOperationResponse(message="Ok", status=StatusEnum.Ok)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.delete("/{user_id}", name="v1:users:remove_user_by_id")
async def remove_user(
    response: Response,
    user_id: str,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
) -> CommonOperationResponse:
    try:
        if get_app_settings().db_mode == ApplicationDBTypes.device:
            await api_wrapper.remove_user(user_id=user_id)
        else:
            await api_wrapper.remove_host_user(user_id=user_id)

        response.status_code = status.HTTP_200_OK
        return CommonOperationResponse(message="Ok", status=StatusEnum.Ok)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
