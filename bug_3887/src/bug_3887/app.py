from litestar import Litestar, MediaType, Request, Router, get
from litestar.openapi import OpenAPIConfig
import aioredis
from litestar.channels.backends.redis import RedisChannelsPubSubBackend
from litestar.config.cors import CORSConfig
from litestar.channels import ChannelsPlugin
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.static_files import create_static_files_router
from contextlib import asynccontextmanager
from litestar import WebSocket, websocket_listener
from collections.abc import AsyncGenerator
from litestar.exceptions.websocket_exceptions import WebSocketDisconnect


cors_config = CORSConfig(
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@get("/user", media_type=MediaType.JSON, tags=["General"])
async def user(request: Request) -> str:
    user = request.user
    return user


@asynccontextmanager
async def chat_room_lifespan(
    socket: WebSocket, channels: ChannelsPlugin, chat_id: str
) -> AsyncGenerator[None, None]:
    async with channels.start_subscription(chat_id) as subscriber:
        try:
            async with subscriber.run_in_background(socket.send_data):
                yield
        except WebSocketDisconnect:
            return


@websocket_listener(
    path="/ws/{chat_id:str}",
    connection_lifespan=chat_room_lifespan,
    exclude_from_auth=True,
)
async def handler(
    data: str,
    chat_id: str,
) -> str:
    print(data)
    return data


redis_instance = aioredis.from_url("redis://localhost:6379/1")
channels_plugin = ChannelsPlugin(
    backend=RedisChannelsPubSubBackend(redis=redis_instance),
    arbitrary_channels_allowed=True,
    create_ws_route_handlers=False,
)
api_router = Router(
    path="/api",
    route_handlers=[
        handler,
        user,
        create_static_files_router(
            path="/public", directories=["public"], guards=None, html_mode=False
        ),
    ],
)


app = Litestar(
    cors_config=cors_config,
    route_handlers=[api_router],
    openapi_config=OpenAPIConfig(
        title="API",
        path="/api",
        version="1.0.0",
        create_examples=True,
        render_plugins=[SwaggerRenderPlugin(path="/schema/swagger")],
    ),
    plugins=[channels_plugin],
)
