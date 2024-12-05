import json

from fastapi.openapi.utils import get_openapi

from rsid_rest.main import app


def export_openapi(export_file_path: str = 'openapi.json') -> None:
    api = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
        # webhooks=app.webhooks,
        tags=app.openapi_tags,
        servers=app.servers,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        separate_input_output_schemas=app.separate_input_output_schemas
    )

    with open(export_file_path, 'w') as f:
        json.dump(api, f, indent=4)
    print(f"Exported file '{export_file_path}'")
