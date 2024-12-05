# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from functools import lru_cache

from rsid_rest.core.settings.app import AppSettings
from rsid_rest.core.settings.base import AppEnvTypes, BaseAppSettings
from rsid_rest.core.settings.development import DevAppSettings
from rsid_rest.core.settings.production import ProdAppSettings
from rsid_rest.core.settings.test import TestAppSettings

environments: dict[AppEnvTypes, type[AppSettings]] = {
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
