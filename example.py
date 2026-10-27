"""Quickstart example for the Bremlio Python client.
Run with: BREMLIO_API_KEY=your_key python example.py
"""
import os

from bremlio import Bremlio


def main():
    bremlio = Bremlio(os.environ.get("BREMLIO_API_KEY"))

    # Send a single SMS to a UK mobile.
    sent = bremlio.send_sms(to="+447700900123", message="Hello from Bremlio!")
    print("sent:", sent)

    # Send and verify a one-time passcode.
    otp = bremlio.send_otp("+447700900123")
    print("otp sent:", otp)
    # In a real app, read the code the user received, then:
    # check = bremlio.verify_otp(otp["verification_id"], "123456")
    # print("verified:", check)

    # Check remaining credits.
    bal = bremlio.balance()
    print("credits:", bal["credits"])


if __name__ == "__main__":
    main()
