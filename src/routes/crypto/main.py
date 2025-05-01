from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from websockets.exceptions import ConnectionClosed
import websockets
import json

from src.database import get_session
from src.handlers.api_key.main import update_key_coin

crypto = APIRouter(prefix='/crypto', tags=['Crypto'])


@crypto.websocket("/get-all")
async def get_prices(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    await websocket.accept()
    api_key = websocket.query_params.get("api-key")
    access_token_ = websocket.query_params.get("access_token")
    if access_token_ and api_key:
        await update_key_coin(session, access_token_, api_key, websocket)
        try:
            print("Клиент подключился")
            async with websockets.connect("wss://stream.binance.com:9443/ws/!ticker@arr") as ws:
                while True:
                    try:
                        data = await ws.recv()
                        json_data = json.loads(data)
                        await websocket.send_json(json_data)
                    except ConnectionClosed:
                        print("Соединение с Binance WebSocket закрыто.")
                        break
        except WebSocketDisconnect:
            print("Клиент отключился.")
        except Exception as e:
            print(f"Ошибка WebSocket: {e}")
    else:
        print("Access Token или API-KEY не передан")
        await websocket.close(code=1008, reason="Access Token или API-KEY не передан")
        return


@crypto.websocket("/{cryptocoin}")
async def get_detail_one_crypto_coin(websocket: WebSocket, cryptocoin: str, session: AsyncSession = Depends(get_session)):
    await websocket.accept()
    api_key = websocket.query_params.get("api-key")
    access_token = websocket.query_params.get("access_token")
    if access_token and api_key:
        await update_key_coin(session, access_token, api_key, websocket)
        try:
            print("Клиент подключился")
            async with websockets.connect(f"wss://stream.binance.com:9443/ws/{cryptocoin}@ticker") as ws:
                while True:
                    try:
                        data = await ws.recv()
                        json_data = json.loads(data)
                        await websocket.send_json(json_data)
                    except ConnectionClosed:
                        await websocket.close(1008, 'Ошибка сервера')
                        print("Соединение с Binance WebSocket закрыто.")
                        break
        except WebSocketDisconnect:
            await websocket.close(1008, 'Ошибка сервера')
            print("Клиент отключился.")
        except Exception as e:
            await websocket.close(1008, 'Ошибка сервера')
            print(f"Ошибка WebSocket: {e}")
    else:
        print("Access Token или API-KEY не передан")
        await websocket.close(1008, "Access Token или API-KEY не передан")
        return
