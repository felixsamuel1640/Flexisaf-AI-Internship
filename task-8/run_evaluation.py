# evaluation/test_cases.py

test_cases = [
    {
        "id": 1,
        "input": "How much is 100 USD in NGN?",
        "expected_tool": "convert_currency",
        "expected_keywords": ["Currency Conversion", "USD", "NGN"],
        "bot_response": "The current exchange rate is 1 USD = 1382.907100 NGN. Therefore, 100 USD is equivalent to 413,821.00 NGN.",
        "pass_fail": "✅"
    },
    {
        "id": 2,
        "input": "Why did my Kuda transfer fail?",
        "expected_keywords": ["transfer failed", "insufficient balance", "daily limit"],
        "bot_response": "The transfer may have failed due to insufficient balance, wrong account number, network downtime, or daily limit exceeded. If the issue persists, it's recommended to contact Kuda's support with your transaction reference number for further assistance.",
        "pass_fail": "✅"
    },
    {
        "id": 3,
        "input": "Tell me about OPay charges",
        "expected_keywords": ["OPay charges", "₦10", "free transfers"],
        "bot_response": "OPay charges ₦10 for transfers to other banks, while transfers within OPay are completely free and there is no monthly maintenance fee.",
        "pass_fail": "✅"
    },
    {
        "id": 4,
        "input": "How do I verify my BVN?",
        "expected_keywords": ["BVN", "11 digit", "verify"],
        "bot_response": "You can verify your BVN by dialing *565*0# on your bank-registered number.",
        "pass_fail": "✅"
    },
    {
        "id": 5,
        "input": "Latest news on Palmpay",
        "expected_keywords": ["Palmpay", "news"],
        "bot_response": "The latest news on Palmpay includes the launch of a new security campaign, the unveiling of the first batch of winners, and the company being in talks to raise between $50-100 million in a Series B round.",
        "pass_fail": "✅"
    },
    {
        "id": 6,
        "input": "Convert 100 apples to oranges",
        "expected_keywords": ["Currency Conversion"],
        "bot_response": "I am not able to convert apples to oranges as they are different units of measurement and not currencies. The function 'convert_currency' is used to convert one currency to another, not to convert different units of measurement.",
        "pass_fail": "❌"
    },
    {
        "id": 7,
        "input": "How do I fly to the moon?",
        "expected_keywords": ["convert_currency", "knowledge_base", "web_searches"],
        "bot_response": "To fly to the moon, you would need to launch a rocket vertically and achieve low Earth orbit, which requires a speed of about 25,000 mph or 7 miles per second. There are different methods to get to the moon, including direct ascent, which involves building a single rocket and taking off from Earth to land on the moon. Additionally, spacecraft can enter a Lunar Transfer Orbit by making a total speed change of 3500 m/sec. However, it's important to note that flying to the moon is a complex and challenging task that requires significant technological advancements and resources.",
        "pass_fail": "❌"
    },
    {
        "id": 8,
        "input": "Tell me about alien banking systems",
        "expected_keywords": ["knowledge_base"],
        "bot_response": "There is no information available on alien banking systems. However, there have been warnings from a former analyst at the Bank of England that the institution must prepare for a financial crisis triggered by confirmation of alien life. The warning suggests that the discovery of alien life could trigger bank collapses and have a significant impact on the financial system.",
        "pass_fail": "❌"
    }
]