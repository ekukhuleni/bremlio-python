"""bremlio: a tiny client for the Bremlio UK SMS and OTP API.

Bremlio is a UK SMS and OTP API (UK +44 mobiles only). This wrapper covers the
public send and verify endpoints.

API base:   https://api.bremlio.com
Auth:       X-Api-Key header (get a key free at https://www.bremlio.com/dashboard.html)

Endpoints used (verified against the live API):
  POST /v1/messages        send one SMS
  POST /v1/messages/bulk   send many in one call
  POST /v1/otp/send        send a one-time passcode
  POST /v1/otp/verify      verify a one-time passcode
  GET  /v1/balance         check remaining credits
"""
import os

import requests

__version__ = "0.1.0"

DEFAULT_BASE_URL = "https://api.bremlio.com"


class BremlioError(Exception):
    """Raised when the Bremlio API returns a non-2xx response."""

    def __init__(self, message, status=None, body=None):
        super().__init__(message)
        self.status = status
        self.body = body


class Bremlio:
    """Client for the Bremlio UK SMS and OTP API.

    Args:
        api_key: Your Bremlio API key. Falls back to the BREMLIO_API_KEY env var.
        base_url: Override the API base URL.
        timeout: Per-request timeout in seconds (default 30).
    """

    def __init__(self, api_key=None, base_url=DEFAULT_BASE_URL, timeout=30):
        api_key = api_key or os.environ.get("BREMLIO_API_KEY")
        if not api_key:
            raise BremlioError("Missing API key. Pass one or set BREMLIO_API_KEY.")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {"Content-Type": "application/json", "X-Api-Key": api_key}
        )

    def _request(self, method, path, json_body=None):
        resp = self._session.request(
            method, self.base_url + path, json=json_body, timeout=self.timeout
        )
        try:
            data = resp.json()
        except ValueError:
            data = None
        if not resp.ok:
            msg = (data or {}).get("error") or (data or {}).get("message") or (
                "HTTP %s" % resp.status_code
            )
            raise BremlioError(msg, status=resp.status_code, body=data)
        return data

    def send_sms(self, to, message, marketing=None, sender_id=None, test=None):
        """Send a single SMS to a UK mobile (+44).

        Returns a dict:
          {success, message_id, provider_message_id, status, segments, credits_remaining}
        """
        body = {"to": to, "message": message}
        if marketing is not None:
            body["marketing"] = marketing
        if sender_id is not None:
            body["sender_id"] = sender_id
        if test is not None:
            body["test"] = test
        return self._request("POST", "/v1/messages", body)

    def send_bulk(self, messages):
        """Send many messages in one call.

        Args:
            messages: list of {"to": ..., "message": ...} dicts.
        """
        return self._request("POST", "/v1/messages/bulk", {"messages": messages})

    def send_otp(self, to):
        """Send a one-time passcode by SMS to a UK mobile.

        Returns {verification_id, test_mode, note}.
        """
        return self._request("POST", "/v1/otp/send", {"to": to})

    def verify_otp(self, verification_id, code):
        """Verify a one-time passcode. Returns {"verified": True} on success."""
        return self._request(
            "POST", "/v1/otp/verify", {"verification_id": verification_id, "code": code}
        )

    def balance(self):
        """Get the account balance and status.

        Returns {credits, email, company, low_credit, kyc_status, ...}.
        """
        return self._request("GET", "/v1/balance")
