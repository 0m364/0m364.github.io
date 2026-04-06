import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock qrcode before importing generate_qr
mock_qrcode_module = MagicMock()
sys.modules['qrcode'] = mock_qrcode_module
sys.modules['qrcode.constants'] = mock_qrcode_module.constants

import generate_qr

class TestGenerateQR(unittest.TestCase):

    def setUp(self):
        # Reset the mock before each test
        mock_qrcode_module.reset_mock()
        mock_qrcode_module.QRCode.return_value.reset_mock()

    def test_generate_url_qr(self):
        # Setup mock
        mock_qrcode = mock_qrcode_module.QRCode
        mock_instance = mock_qrcode.return_value
        mock_img = MagicMock()
        mock_instance.make_image.return_value = mock_img

        # Call the function
        url = "https://example.com"
        output = "test_url_qr.png"
        generate_qr.generate_url_qr(url, output)

        # Assertions
        mock_qrcode.assert_called_with(
            version=1,
            error_correction=mock_qrcode_module.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        mock_instance.add_data.assert_called_once_with(url)
        mock_instance.make.assert_called_once_with(fit=True)
        mock_instance.make_image.assert_called_once_with(fill_color="black", back_color="white")
        mock_img.save.assert_called_once_with(output)

    def test_generate_vcard_qr(self):
        # Setup mock
        mock_qrcode = mock_qrcode_module.QRCode
        mock_instance = mock_qrcode.return_value
        mock_img = MagicMock()
        mock_instance.make_image.return_value = mock_img

        # Call the function
        name = "John Doe"
        org = "Example Corp"
        title = "Engineer"
        email = "john@example.com"
        url = "https://example.com"
        output = "test_vcard_qr.png"

        generate_qr.generate_vcard_qr(name, org, title, email, url, output)

        # Assertions
        mock_qrcode.assert_called_with(
            version=1,
            error_correction=mock_qrcode_module.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Verify vCard format
        expected_vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;;
FN:{name}
ORG:{org}
TITLE:{title}
EMAIL;type=INTERNET;type=WORK;type=pref:{email}
URL:{url}
END:VCARD"""
        mock_instance.add_data.assert_called_once_with(expected_vcard)
        mock_instance.make.assert_called_once_with(fit=True)
        mock_instance.make_image.assert_called_once_with(fill_color="black", back_color="white")
        mock_img.save.assert_called_once_with(output)


    def test_generate_vcard_qr_sanitization(self):
        # Setup mock
        mock_qrcode = mock_qrcode_module.QRCode
        mock_instance = mock_qrcode.return_value
        mock_img = MagicMock()
        mock_instance.make_image.return_value = mock_img

        # Call the function with injected newlines
        name = "John\nDoe"
        org = "Example\r\nCorp"
        title = "Engi\nneer"
        email = "john\n@example.com"
        url = "https://example.com\n/evil"
        output = "test_vcard_qr_sanitized.png"

        generate_qr.generate_vcard_qr(name, org, title, email, url, output)

        # Verify vCard format does not contain newlines in fields
        expected_name = "JohnDoe"
        expected_org = "ExampleCorp"
        expected_title = "Engineer"
        expected_email = "john@example.com"
        expected_url = "https://example.com/evil"

        expected_vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{expected_name};;;;
FN:{expected_name}
ORG:{expected_org}
TITLE:{expected_title}
EMAIL;type=INTERNET;type=WORK;type=pref:{expected_email}
URL:{expected_url}
END:VCARD"""
        mock_instance.add_data.assert_called_once_with(expected_vcard)

    @patch('generate_qr.generate_url_qr')
    @patch('sys.argv', ['generate_qr.py', 'url', 'https://example.com', '-o', 'custom_output.png'])
    def test_main_url_command(self, mock_generate_url_qr):
        generate_qr.main()
        mock_generate_url_qr.assert_called_once_with('https://example.com', 'custom_output.png')

    @patch('generate_qr.generate_vcard_qr')
    @patch('sys.argv', ['generate_qr.py', 'vcard', '--name', 'John Doe', '--org', 'Example Corp', '--title', 'Engineer', '--email', 'john@example.com', '--url', 'https://example.com', '-o', 'vcard_output.png'])
    def test_main_vcard_command(self, mock_generate_vcard_qr):
        generate_qr.main()
        mock_generate_vcard_qr.assert_called_once_with(
            'John Doe', 'Example Corp', 'Engineer', 'john@example.com', 'https://example.com', 'vcard_output.png'
        )

    @patch('generate_qr.generate_vcard_qr')
    @patch('generate_qr.generate_url_qr')
    @patch('sys.argv', ['generate_qr.py'])
    def test_main_no_command_default_behavior(self, mock_generate_url_qr, mock_generate_vcard_qr):
        generate_qr.main()
        # Verify both examples are generated
        mock_generate_url_qr.assert_called_once_with('https://example.com', 'example_url_qr.png')
        mock_generate_vcard_qr.assert_called_once_with(
            "John Doe", "Example Corp", "Software Engineer", "john@example.com", "https://example.com", "example_vcard_qr.png"
        )

if __name__ == "__main__":
    unittest.main()
