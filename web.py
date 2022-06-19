from typing import Optional

from fastapi import APIRouter, Depends, Query

from core.blockchain import BlockChain
from utils.exceptions import UNAUTHORIZED

router = APIRouter(prefix='/api/v1')


async def check_key(key: Optional[str] = Query(None)):
    if not key:
        raise UNAUTHORIZED
    return key


block_chain = BlockChain()


@router.get('/mine')
async def mine():
    return ''
