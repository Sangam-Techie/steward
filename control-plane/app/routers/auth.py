import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models.identity import Device, User
from ..schemas.devices import DeviceRegisterRequest, DeviceRegisterResponse
from ..security import create_device_token, hash_token

router = APIRouter(tags=["auth"])


# Reusable type alias (optional, but clean across multiple routes)
DBSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("/api/v1/auth/device/register", response_model=DeviceRegisterResponse)
async def register_device(
    payload: DeviceRegisterRequest,
    session: DBSession,  # <-- No function call in default value!)
):
    result = await session.execute(
        select(User).where(User.email == "sangamaryal1111@gmail.com")
    )
    user = result.scalar_one_or_none()
    if user is None:
        user = User(id=uuid.uuid4(), email="sangamaryal1111@gmail.com")
        session.add(user)

    device_id = uuid.uuid4()
    token = create_device_token(str(device_id), payload.platform)
    hashed = hash_token(token)

    # Contruct device entity
    device = Device(
        id=device_id,
        user_id=user.id,
        name=payload.name,
        platform=payload.platform,
        token_hash=hashed,
    )
    session.add(device)
    await session.commit()

    # Return plaintext token once; hash persists in database
    return DeviceRegisterResponse(device_id=str(device.id), device_token=token)
