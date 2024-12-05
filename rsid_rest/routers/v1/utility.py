# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import tempfile
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Response, UploadFile, status
from loguru import logger

from rsid_rest.rsid_lib.models import FWUpdateStatusReportResponse, UpdateCheckerResponse
from rsid_rest.rsid_lib.rsid_api_wrapper import RSIDApiWrapper, get_rsid_api

router = APIRouter(
    prefix="/utility",
    tags=["utility"],
)


@router.get(
    "/update-status/",
    name="v1:utility:get-software-update-status",
    summary="Retrieve local and remote software & firmware versions and whether an update is available.",
    description="Retrieve local and remote software & firmware versions and whether an update is available. "
                "\n\n",
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
def query_update_status(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)]
) -> UpdateCheckerResponse:
    try:
        update_status = api_wrapper.query_update_status()
        response.status_code = status.HTTP_200_OK
        return update_status
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


async def delete_temp_uploads(uploaded_file: Path | None) -> None:
    if uploaded_file is not None and uploaded_file.exists():
        try:
            logger.info(f"Deleting temporary file {uploaded_file.name}")
            uploaded_file.unlink(missing_ok=True)
        except OSError as os_e:
            logger.error(os_e)


@router.post(
    "/fw-update-report/",
    name="v1:utility:fw-update-report",
    summary="Retrieve if FW update file is compatible with device and reports FW/SW compatibility.",
    description="Retrieve if FW update file is compatible with device and reports FW/SW compatibility. "
                "\n\n",
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
async def query_fw_update_status(
    response: Response,
    api_wrapper: Annotated[RSIDApiWrapper, Depends(get_rsid_api)],
    background_tasks: BackgroundTasks,
    file: Annotated[
        UploadFile,
        File(
            title="Firmware binary file",
            description="Firmware binary file",
        ),
    ],
) -> FWUpdateStatusReportResponse:
    temp_path: Path | None
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
        result = await api_wrapper.query_fw_update_status(file_path=temp_path)
        background_tasks.add_task(delete_temp_uploads, uploaded_file=temp_path)
        return result
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
