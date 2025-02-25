import urllib.parse

from typing import List, Dict, Any


import httpx


class QueryAdapter:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_db_structure(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/queries/db_structure/")
            response.raise_for_status()
            return response.json()

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            query = urllib.parse.quote(query)
            response = await client.post(f"{self.base_url}/queries/execute_query/?query={query}")
            response.raise_for_status()
            return response.json()["results"]
