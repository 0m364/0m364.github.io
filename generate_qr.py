import qrcode
import argparse
import sys

def generate_url_qr(url, output_filename="website_qr.png"):
    """Generates a QR code that redirects to a given URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_filename)
    print(f"Generated {output_filename} for URL: {url}")

def generate_vcard_qr(name, organization, title, email, url, output_filename="vcard_qr.png"):
    """Generates a digital business card (vCard) QR code."""
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;;
FN:{name}
ORG:{organization}
TITLE:{title}
EMAIL;type=INTERNET;type=WORK;type=pref:{email}
URL:{url}
END:VCARD"""

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_filename)
    print(f"Generated {output_filename} with vCard contact details.")

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes for URLs and vCards.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # URL command
    url_parser = subparsers.add_parser("url", help="Generate a QR code for a URL")
    url_parser.add_argument("url", help="The URL to encode")
    url_parser.add_argument("-o", "--output", default="website_qr.png", help="Output filename")

    # vCard command
    vcard_parser = subparsers.add_parser("vcard", help="Generate a vCard QR code")
    vcard_parser.add_argument("--name", required=True, help="Full name")
    vcard_parser.add_argument("--org", required=True, help="Organization name")
    vcard_parser.add_argument("--title", required=True, help="Job title")
    vcard_parser.add_argument("--email", required=True, help="Email address")
    vcard_parser.add_argument("--url", required=True, help="Website URL")
    vcard_parser.add_argument("-o", "--output", default="vcard_qr.png", help="Output filename")

    args = parser.parse_args()

    if args.command == "url":
        generate_url_qr(args.url, args.output)
    elif args.command == "vcard":
        generate_vcard_qr(args.name, args.org, args.title, args.email, args.url, args.output)
    else:
        # Default behavior: demonstrate with example data if no arguments provided
        print("No command provided. Running default example...")
        example_url = "https://example.com"
        generate_url_qr(example_url, "example_url_qr.png")
        generate_vcard_qr("John Doe", "Example Corp", "Software Engineer", "john@example.com", example_url, "example_vcard_qr.png")
        print("\nRun `python generate_qr.py -h` for usage instructions.")

if __name__ == "__main__":
    main()
