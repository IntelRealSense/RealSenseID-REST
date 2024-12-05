# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from typing import Any

from pydantic import ValidationError
from pydantic_core.core_schema import ValidationInfo, ValidatorFunctionWrapHandler

from . import rsid_py


# TODO: Refactor validators


def algo_flow_validator(v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo) -> rsid_py.AlgoFlow:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())

    if isinstance(v, rsid_py.AlgoFlow):
        return v

    if isinstance(v, str):
        values = {}
        for enum_val in rsid_py.AlgoFlow.__members__:
            values["AlgoFlow." + str(enum_val)] = rsid_py.AlgoFlow.__members__[enum_val]
        if v in values.keys():
            return values[v]
        else:
            raise ValueError(
                f"algo_flow received unexpected value of type: {type(v)}" " - expected one of: " + ", ".join(values)
            )
    raise ValueError(f"algo_flow - received unexpected type: {type(v)}")


def camera_rotation_validator(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> rsid_py.CameraRotation:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())

    if isinstance(v, rsid_py.CameraRotation):
        return v

    if isinstance(v, str):
        values = {}
        for enum_val in rsid_py.CameraRotation.__members__:
            values["CameraRotation." + str(enum_val)] = rsid_py.CameraRotation.__members__[enum_val]
        if v in values.keys():
            return values[v]
        else:
            raise ValueError(
                f"camera_rotation received unexpected value of type: {type(v)}"
                " - expected one of: " + ", ".join(values)
            )
    raise ValueError(f"camera_rotation - received unexpected type: {type(v)}")


def face_selection_policy_validator(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> rsid_py.FaceSelectionPolicy:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())

    if isinstance(v, rsid_py.FaceSelectionPolicy):
        return v

    if isinstance(v, str):
        values = {}
        for enum_val in rsid_py.FaceSelectionPolicy.__members__:
            values["FaceSelectionPolicy." + str(enum_val)] = rsid_py.FaceSelectionPolicy.__members__[enum_val]
        if v in values.keys():
            return values[v]
        else:
            raise ValueError(
                f"face_selection_policy received unexpected value of type: {type(v)}"
                " - expected one of: " + ", ".join(values)
            )
    raise ValueError(f"face_selection_policy - received unexpected type: {type(v)}")


def security_level_policy_validator(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> rsid_py.SecurityLevel:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())

    if isinstance(v, rsid_py.SecurityLevel):
        return v

    if isinstance(v, str):
        values = {}
        for enum_val in rsid_py.SecurityLevel.__members__:
            values["SecurityLevel." + str(enum_val)] = rsid_py.SecurityLevel.__members__[enum_val]
        if v in values.keys():
            return values[v]
        else:
            raise ValueError(
                f"security_level received unexpected value of type: {type(v)}"
                " - expected one of: " + ", ".join(values)
            )
    raise ValueError(f"security_level - received unexpected type: {type(v)}")


def matcher_confidence_level_validator(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> rsid_py.MatcherConfidenceLevel:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())

    if isinstance(v, rsid_py.MatcherConfidenceLevel):
        return v

    if isinstance(v, str):
        values = {}
        for enum_val in rsid_py.MatcherConfidenceLevel.__members__:
            values["MatcherConfidenceLevel." + str(enum_val)] = rsid_py.MatcherConfidenceLevel.__members__[enum_val]
        if v in values.keys():
            return values[v]
        else:
            raise ValueError(
                f"security_level received unexpected value of type: {type(v)}"
                " - expected one of: " + ", ".join(values)
            )
    raise ValueError(f"matcher_confidence_level - received unexpected type: {type(v)}")
