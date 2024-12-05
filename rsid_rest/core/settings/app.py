# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
from pathlib import Path
from pprint import pformat
from typing import Annotated, Any

from asgi_correlation_id.context import correlation_id
from loguru import logger
from pydantic import Field

from rsid_rest import __version__
from rsid_rest.core.logging import InterceptHandler
from rsid_rest.core.settings.base import (
    ApplicationDBTypes,
    BaseAppSettings,
    HostModeAuthTypes, StreamEncodingStypes,
)


class AppSettings(BaseAppSettings, validate_assignment=True):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "RealSenseID API"
    description: str = "RealSenseID API"
    version: str = __version__

    api_prefix: str = "/api"
    api_v1_prefix: str = "/v1"

    allowed_hosts: list[str] = ["*"]

    # Device discovery and serial port configuration
    auto_detect: bool = True
    com_port: str | None = None
    preview_camera_number: int = -1  # -1 = auto-detect

    # DB mode
    db_mode: ApplicationDBTypes = ApplicationDBTypes.device

    # DB Host mode configuration
    db_file: Path | None = "vectors.db"
    host_mode_auth_type: HostModeAuthTypes = HostModeAuthTypes.hybrid

    # Hybrid mode settings
    """" Maximum number of faceprints to be sent to device after vector db search """
    host_mode_hybrid_max_results: int | None = 10
    """" Vector DB threshold for searching. """
    host_mode_hybrid_score_threshold: float | None = 0.2

    # Preview and streaming configuration
    preview_jpeg_quality: Annotated[int, Field(ge=1, le=100)] = 80  # 1 - 100
    """ JPEG performance is better with TurboJPEG than WebP with OpenCV """
    preview_stream_type: StreamEncodingStypes = StreamEncodingStypes.jpeg
    preview_webp_quality: Annotated[int, Field(ge=1, le=100)] = 90  # 1 - 100

    logging_level: int = logging.INFO
    loggers: list[str] = ["uvicorn.asgi", "uvicorn.access", "authlib"]

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
            "contact": {
                "name": "Intel RealSense",
                "url": "https://www.intelrealsense.com/",
            },
            "license_info": {
                "name": "Intel RealSenseID EULA",
                "url": "https://www.intelrealsense.com/intel-realsense-id-eula/",
            },
            # If we want to enable token/api-key at some point. Here's how to show it in the docs
            # swagger_ui_parameters={
            #     'Bearer': {
            #         'type': 'apiKey',
            #         'name': 'Authorization',
            #         'in': 'header',
            #         'description': '<hr/>'
            #                        'Enter the word <tt>Token</tt> followed by space then your apiKey <br/><br/> '
            #                        '<b>Example:</b> <pre>Token f4bff35e0f6427860ae31bde0b5f2352cbf73d80</pre>'
            #                        '<hr/><br/>'
            #     }
            # }
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]

        def correlation_id_filter(record):
            record["correlation_id"] = correlation_id.get()
            return record["correlation_id"]

        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(
            handlers=[
                {
                    "sink": sys.stderr,
                    "level": self.logging_level,
                    "format": format_record,
                    "filter": correlation_id_filter,
                }
            ]
        )


def format_record(record: dict) -> str:  # pragma: no cover
    format_string = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>[{correlation_id}]</cyan> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(record["extra"]["payload"], indent=4, compact=True, width=88)
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string
