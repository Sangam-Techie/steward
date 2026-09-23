from pydantic import BaseModel


class DeviceRegisterRequest(BaseModel):
    name: str
    platform: str


class DeviceRegisterResponse(BaseModel):
    device_id: str
    device_token: str
