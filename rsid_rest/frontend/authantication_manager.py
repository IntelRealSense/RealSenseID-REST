# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import httpx
from nicegui import ui

from rsid_rest.frontend.users_manager import UserManager


class AuthenticationManager:
    def __init__(self, base_url: str, user_manager: UserManager) -> None:
        self.loading_notification = None
        self.base_url = base_url
        self.http_client: httpx.AsyncClient = httpx.AsyncClient()
        self._status_label: ui.label | None = None
        self._preview_image: ui.interactive_image | None = None
        self.preview_image_content: str = ""
        self.status_label_text: str = ""
        self.user_manager = user_manager

    @property
    def preview_image(self) -> ui.interactive_image | None:
        return self._preview_image

    @preview_image.setter
    def preview_image(self, p):
        self._preview_image = p
        self._preview_image.bind_content_from(self, "preview_image_content")

    @property
    def status_label(self) -> ui.label | None:
        return self._status_label

    @status_label.setter
    def status_label(self, p):
        self._status_label = p
        self._status_label.bind_text(self, "status_label_text")

    def clear_auth_result(self) -> None:
        self.preview_image_content = ""
        self.status_label_text = "RealSenseID Ready"
        # self._preview_image.content = self.preview_image_content
        # self._preview_image.bind_content_from(self, 'preview_image_content')
        # self._status_label.set_text('RealSenseID Ready')

    async def authenticate(self) -> None:
        self.loading_notification = ui.notification("⚡ Authenticating", spinner=True)
        self.clear_auth_result()

        response: httpx.Response = await self.http_client.get(f"{self.base_url}/v1/auth/", timeout=30)

        self.loading_notification.dismiss()

        if response.status_code in [200, 406]:
            # log.push(response.text)
            if response.json()["status"] == "AuthenticateStatus.Success":
                self.status_label_text = response.json()["status"] + " :" + response.json()["user_id"]
                ui.notify(
                    response.json()["status"] + " :" + response.json()["user_id"],
                    color="positive",
                )
            else:
                ui.notify(response.json()["status"], color="negative")
                self.status_label_text = response.json()["status"]

            # Render faces if any - this can also be tru on status failure
            user_id = response.json()["user_id"]
            faces: dict | None = response.json()["faces"]
            preview_image_overlay = ""
            if faces is not None:
                for face in faces:
                    x = face["x"]
                    y = face["y"]
                    w = face["w"]
                    h = face["h"]
                    preview_image_overlay = preview_image_overlay + (
                        f'<rect id="{user_id}" x="{x}" y="{y}" width="{w}" height="{h}" '
                        'fill="none" stroke="yellow" pointer-events="all" cursor="pointer" />'
                    )
            self.preview_image_content = preview_image_overlay

            ui.timer(3, lambda: self.clear_auth_result(), once=True)
        else:
            ui.notify(
                f"Error while communicating with API endpoint. Status: {response.status_code}",
                color="negative",
            )

    def render_controls(self) -> None:
        ui.label("User Authentication").classes("font-medium")
        ui.button("Authenticate", on_click=self.authenticate).classes("w-full").bind_enabled(
            self.user_manager.users_list,
            backward=lambda x: len(self.user_manager.users_list.users) > 0,
        )
