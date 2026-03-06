
import os, requests
from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from knowledge import knowledge_base
from langchain_tavily import TavilySearch

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

api_key = os.getenv('EXCHANGE_API_KEY')

# llm setup
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

# TOOL 1: EXCHANGE RATE:
@tool
def convert_currency(amount, from_currency: str, to_currency: str) -> str:
    """
    Convert money from one currency to another.
    Use when user asks to convert money, check exchange rates,
    or ask how much naira they will get for dollars, pounds etc.

    Example inputs:
    amounts=100, from_currency="USD", to_currency="NGN"
    amount=50, from_currency="EUR", to_currency="GBP"
    """

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return "❌ Invalid amount! Please provide a numeric value."

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Unable to fetch exchange rate right now"

        data = response.json()

        if data["result"] != "success":
            return f"Exchange API error! from {from_currency} - {to_currency}"

        rate = data["conversion_rate"]

        converted = amount * rate

        return (
            f"**Currency Conversion**\n"
            f"{amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}\n"
            f"Rate 1 {from_currency} = {rate:.6f} {to_currency}"
        )

    except Exception as e:
        return f"Error converting currency {str(e)}"


# TOOL 2: KNOWLEDGE BASE
@tool
def search_knowledge_base(query: str) -> str:
    """
    Use when user asks about nigerian fintech apps like Opay, Palmpay,
    Kuda - including failed transfers, bank charges, transfer limits,
    BVN, KYC verification, or comparing nigerian banking apps.
    Input should be smart description of what user wants to know.
    """

    query = query.lower()

    for key, answer in knowledge_base.items():
        if any(word in query.lower() for word in key.split()):
            return answer

    return (
        "I don't have that in my knowledge base yet"
        "Try asking about Kuda, Palmpay, Kuda, transfer failures,"
        "BVN or exchange rates"
    )

# TOOL 3: TAVILY WEB SEARCH
web_search = TavilySearch(
    max_results=3,
    description=(
        "Use for current nigerian fintect news, lates Opay and Palmpay updates,"
        "Black market exchange rates or any financial information, "
        "not covered by the other tools."
    )
)



