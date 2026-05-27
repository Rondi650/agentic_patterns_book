import os
os.system('clear')

print('\nx\n')


# --- Placeholder for external interaction ---
def http_post(url, data, headers):
    print(f"PROXY: Calling external API at {url}...")
    # Simulate a complex response from the external API
    return {"external_status": "OK", "data": {"one_time_code": "APPLIED123", "valid_until": "2025-09-22"}}


# --- Resides in the main application context ---
class AirlineBookingAgent:
    def apply_partner_discount(self, user_id, loyalty_code):
        # The primary agent only knows about the internal proxy
        proxy = HotelBonanzaProxyAgent()
        proxy_request = {
            "action": "validate_discount",
            "user_id": user_id,
            "loyalty_code": loyalty_code
        }
        print(proxy_request)
        # The call is simple and uses internal language
        proxy_response = proxy.handle_request(proxy_request)
        return proxy_response.get('discount_code')


# --- Resides in a secure, isolated context ---
class HotelBonanzaProxyAgent:
    def __init__(self):
        # This proxy is the only component with the secret API key
        # self.api_key = load_secret("HOTEL_BONANZA_API_KEY")
        self.api_key = "SECRET_API_KEY"

    def handle_request(self, internal_request: dict):
        # 1. Translate the internal request into the external API format
        external_request = {
            "user": internal_request["user_id"], "code": internal_request["loyalty_code"]}
        print(external_request)
        # 2. Securely call the external system
        external_response = http_post(
            "https://api.hotelbonanza.com/v2/discounts",
            data=external_request,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        # 3. Translate the complex external response back to a simple internal format
        if external_response.get("external_status") == "OK":
            return {"status": "success", "discount_code": external_response["data"]["one_time_code"]}
        else:
            return {"status": "failure", "discount_code": None}


# --- Execute the Workflow ---
booking_agent = AirlineBookingAgent()
discount = booking_agent.apply_partner_discount("user123", "HB-XYZ")
print(f"Booking Agent received discount code: {discount}")

print('\nx\n')
