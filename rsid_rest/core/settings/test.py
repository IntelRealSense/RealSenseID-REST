# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import logging

from pydantic_settings import SettingsConfigDict

from rsid_rest.core.settings.app import AppSettings


class TestAppSettings(AppSettings, validate_assignment=True):
    model_config = SettingsConfigDict(env_file="test.env")

    title: str = "Test RealSenseID API"
    logging_level: int = logging.DEBUG
    debug: bool = True

    auto_detect: bool = True
    com_port: str = "COM5"
