from typing import Callable

from fastapi import FastAPI

from app.db.mongodb import close_mongo_connection, connect_to_mongo

def create_start_app_handler(app: FastAPI) -> Callable:
    """
    Create a function to be called when the application starts.
    """
    async def start_app() -> None:
        await connect_to_mongo()
    
    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    """
    Create a function to be called when the application stops.
    """
    async def stop_app() -> None:
        await close_mongo_connection()
    
    return stop_app 