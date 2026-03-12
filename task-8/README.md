# 🇳🇬 AjoBot Accuracy Test Report

**Date:** 2026-03-12  
**Tester:** felixsamuel1640  

---

## Test Cases

| Test ID | Query | Expected Tool | Expected Keywords | Bot Response (Summary) | 
Pass/Fail |
| ------- | ----- | ------------- | ---------------- | -------------------- | 
---------- |
| 1 | How much is 100 USD in NGN? | convert_currency | Currency Conversion, USD, 
NGN | The current exchange rate is 1 USD = 1382.907100 NGN. Therefore, 100 USD is 
equivalent to 413,821.00 NGN. | ✅ |
| 2 | Why did my Kuda transfer fail? | knowledge_base | transfer failed, 
insufficient balance, daily limit | The transfer may have failed due to 
insufficient balance, wrong account number, network downtime, or daily limit 
exceeded. Contact Kuda's support if needed. | ✅ |
| 3 | Tell me about OPay charges | knowledge_base | OPay charges, ₦10, free 
transfers | OPay charges ₦10 for transfers to other banks, transfers within OPay 
are free, no monthly maintenance fee. | ✅ |
| 4 | How do I verify my BVN? | knowledge_base | BVN, 11 digit, verify | You can 
verify your BVN by dialing *565*0# on your bank-registered number. | ✅ |
| 5 | Latest news on Palmpay | web_searches | Palmpay, news | Latest news: security 
campaign, first batch of winners, company raising $50-100 million Series B. | ✅ |
| 6 | Convert 100 apples to oranges | convert_currency | Currency Conversion | 
Cannot convert apples to oranges; 'convert_currency' only works with currencies. | 
❌ |
| 7 | How do I fly to the moon? | web_searches | convert_currency, knowledge_base, 
web_searches | Bot gave general spaceflight info, not financial info. | ❌ |
| 8 | Tell me about alien banking systems | knowledge_base | knowledge_base | No 
info on alien banking; general warnings from Bank of England analyst. | ❌ |

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | 8 |
| Passed | 5 |
| Failed | 3 |
| Accuracy | 62.5% |

---

### Notes

- ✅ Passed = Bot returned relevant answer matching expected keywords.  
- ❌ Failed = Bot did not provide relevant info or answered outside the scope.  
- This report was manually documented by running the queries in the AjoBot 
application.  

---

