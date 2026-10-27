# bremlio-python

A tiny Python client for the [Bremlio](https://www.bremlio.com) UK SMS and OTP API.

Bremlio is a UK SMS and OTP API: send text messages and one-time passcodes to UK mobile numbers over a simple REST API, pay as you go from 4.65p per SMS. Get a free API key at [bremlio.com/dashboard.html](https://www.bremlio.com/dashboard.html) (25 free credits on signup).

Depends only on `requests`. Python 3.8 or newer.

## Install

This is a small single-file client. Copy `bremlio.py` into your project, or install from the repo:

```bash
pip install git+https://github.com/ekukhuleni/bremlio-python.git
```

## Quickstart

```python
import os
from bremlio import Bremlio

# Reads BREMLIO_API_KEY from the environment, or pass the key directly.
bremlio = Bremlio(os.environ["BREMLIO_API_KEY"])

# Send an SMS to a UK mobile (+44).
res = bremlio.send_sms(to="+447700900123", message="Hello from Bremlio!")
print(res["message_id"], res["credits_remaining"])
```

## Send and verify a one-time passcode

```python
otp = bremlio.send_otp("+447700900123")
# otp["verification_id"]

# After the user enters the code they received:
check = bremlio.verify_otp(otp["verification_id"], "123456")
if check["verified"]:
    print("verified")
```

## Check your balance

```python
bal = bremlio.balance()
print(bal["credits"], bal["kyc_status"])
```

## API

| Method | Calls | Returns |
| --- | --- | --- |
| `send_sms(to, message, marketing=None, sender_id=None, test=None)` | `POST /v1/messages` | `{success, message_id, provider_message_id, status, segments, credits_remaining}` |
| `send_bulk(messages)` | `POST /v1/messages/bulk` | bulk send result |
| `send_otp(to)` | `POST /v1/otp/send` | `{verification_id, test_mode, note}` |
| `verify_otp(verification_id, code)` | `POST /v1/otp/verify` | `{verified}` |
| `balance()` | `GET /v1/balance` | `{credits, email, company, low_credit, kyc_status, ...}` |

All requests send the `X-Api-Key` header against the base URL `https://api.bremlio.com`.

Pass `test=True` to `send_sms` to validate a request without charging credits or sending a real message.

## Notes and limits

- Bremlio sends to UK mobile numbers (+44) only. It does not offer voice, WhatsApp, email or international SMS.
- Non-2xx responses raise `BremlioError` with `.status` and `.body`.
- Never hard-code your API key. Use an environment variable (`BREMLIO_API_KEY`).

## Links

- Website: https://www.bremlio.com
- API docs: https://www.bremlio.com/developers.html
- Pricing: https://www.bremlio.com/pricing/

## License

MIT. See [LICENSE](LICENSE). Bremlio is a product of Bremlio Ltd (UK company number 17444792).
