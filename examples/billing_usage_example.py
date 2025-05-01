import macrocosmos as mc
import os


def main():
    # Initialize the client
    client = mc.BillingClient(api_key=os.environ.get("MACROCOSMOS_API_KEY"))

    # Get usage information for gravity
    response = client.billing.GetUsage()

    # Print the response
    print(f"Available credits: {response.available_credits}")
    print(f"Used credits: {response.used_credits}")
    print(f"Remaining credits: {response.remaining_credits}")
    print("\nBilling rates:")
    for rate in response.billing_rates:
        print(f"  - Rate type: {rate.rate_type}")
        print(f"    Unit size: {rate.unit_size}")
        print(f"    Unit type: {rate.unit_type}")
        print(f"    Price per unit: {rate.price_per_unit} {rate.currency}")


if __name__ == "__main__":
    main()
