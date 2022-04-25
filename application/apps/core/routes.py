from time import sleep

from fastapi import APIRouter

router = APIRouter()


@router.get("/sleep")
def do_sleep():
    sleep(10)
    return {"st": "Done"}


@router.get("/sleep2")
def do_sleep2():
    sleep(10)
    return {"st": "Done"}
