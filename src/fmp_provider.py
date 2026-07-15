import os
import requests
from dotenv import load_dotenv

load_dotenv()


BASE_URL = "https://financialmodelingprep.com/api/v3"


def get_api_key() -> str:
    api_key = os.getenv("FMP_API_KEY")

    if not api_key:
        raise ValueError("Missing FMP_API_KEY in .env file")

    return api_key


def get_income_statement(ticker: str, limit: int = 10) -> list[dict]:
    url = f"{BASE_URL}/income-statement/{ticker}"
    params = {
        "limit": limit,
        "apikey": get_api_key(),
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()


def get_cash_flow_statement(ticker: str, limit: int = 10) -> list[dict]:
    url = f"{BASE_URL}/cash-flow-statement/{ticker}"
    params = {
        "limit": limit,
        "apikey": get_api_key(),
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()