# ReadSenseID FastAPI 

This software is work-in-progress. It aims at providing REST and WebSocket interface 
to the RealSenseID library. 

## Pre-requisites

- Python 3.10+ (All the way to Python 3.12)

## Installation - First Time

Prepare a virtual environment:

Note: If you're on Ubuntu, and it complains about `pip` not available, run this:  
```shell
sudo apt install -y python3-pip
```

Standard installation:

First time only (Linux & Windows):
```shell
python3 -m pip install poetry         # Install poetry
poetry install                        # Install requirements
```

Or you can use the official poetry installer: https://python-poetry.org/docs/#installing-with-the-official-installer
and then:
```shell
poetry install                        # Install requirements
```

## Update / Run

Update Packages (Linux & Windows):
```shell
poetry install                        # Install / Update requirements
```

Then everytime you need to run:
```shell
poe run
```
or
```shell
poetry run fastapi run rsid_rest/main.py 
```
or
```shell
poetry run python3 -m uvicorn rsid_rest.main:app --reload
```

## Usage
### API Documentation
Point your browser to: http://127.0.0.1:8000/docs/
### Sample Frontend
Point your browser to: http://127.0.0.1:8000/gui/

## Configuration and Settings
`.env` files and environment variables can be used to configura the application. The following table shows
the file names for environment files.

### Env files

| Environment |     File      |
|-------------|:-------------:|
| Dev         |    `.env`     |
| Prod        |  `prod.env`   |


### General Settings

The following variables can be set in the `.env` files or passed as Environment Variables before starting the app. 

| Variable                           | Default  | Configuration                                                                                            |
|------------------------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `auto_detect`                      |  `True`  | Automatically detect camera on system. Useful in dev environments                                        |
| `com_port`                         |  `None`  | Specifies COM port when `auto_detect` is False. Windows example: `COM5`                                  |
| `preview_camera_number`            |   `-1`   | Camera index for preview `-1` for auto-detect                                                            |
| `db_mode`                          | `device` | DB location: `device` or `host`                                                                          |

### Host DB Mode Settings

Similar to General Settings, the following variables can be set in `.env` or in the environment variables. They are only effective if `db_mode=host`

| Variable                           | Default  | Configuration                                                                                            |
|------------------------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `host_mode_auth_type`              | `hybrid` | In `host` DB mode: `hybrid`: use vector DB to enhance performance or: `device`: only use device matcher. |
| `host_mode_hybrid_max_results`     |   `10`   | In `host` and `hybrid`: Vector DB filters should filter for a max of X candidates                        |
| `host_mode_hybrid_score_threshold` |  `0.2`   | In `host` and `hybrid`: Vector DB filters should filter use this score threshold (keep low)              |


### Streaming Settings

Similar to General Settings, the following variables can be set in `.env` or in the environment variables.

| Variable                           | Default  | Configuration                                                                                            |
|------------------------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `preview_stream_type`              |  `jpeg`  | Streaming Preview output: `jpeg` or `webp`                                                               |
| `preview_jpeg_quality`             |   `85`   | Streaming Preview JPEG quality. Min: `1`     Max: `100`                                                  |
| `preview_webp_quality`             |   `85`   | Streaming Preview WebP quality. Min: `1`     Max: `100`                                                  |


### Creating a Client using the OpenAPI Schema
Running the following command will generate `openapi.json` file that can be used with the OpenAPI generator
```shell
poe gen-openapi
```
Navigate to: https://github.com/OpenAPITools/openapi-generator?tab=readme-ov-file#overview to find out more about
the ability to automatically generate SDK that can use this API.

---
## TODO:
- [x] Add Setting to switch from auto-detect device to preset device
- [x] Complete API - Cover all device APIs
  - [ ] Add device ping
  - [x] Add enroll from image
  - [x] Add device info (sw/fw version)
  - [x] Add FaceRect to auth response
  - [x] Complete the OpenAPI schema
  - [x] Support preview/streaming
- [x] Properly document all API endpoints
- [x] Add Host mode + vector DB sample
