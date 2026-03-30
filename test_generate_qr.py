import unittest
from unittest.mock import MagicMock, patch
import sys

# Mocking qrcode before importing the module that uses it
sys.modules['qrcode'] = MagicMock()
import qrcode
qrcode.constants = MagicMock()
qrcode.constants.ERROR_CORRECT_L = 'L'

from generate_qr import generate_url_qr, generate_vcard_qr

class TestGenerateQR(unittest.TestCase):

    @patch('generate_qr.qrcode.QRCode')
    def test_generate_url_qr(self, mock_qrcode_class):
        mock_qr = mock_qrcode_class.return_value
        mock_img = MagicMock()
        mock_qr.make_image.return_value = mock_img

        url = "https://example.com"
        output = "test_url.png"

        generate_url_qr(url, output)

        mock_qrcode_class.assert_called_once_with(
            version=1,
            error_correction='L',
            box_size=10,
            border=4,
        )
        mock_qr.add_data.assert_called_once_with(url)
        mock_qr.make.assert_called_once_with(fit=True)
        mock_qr.make_image.assert_called_once_with(fill_color="black", back_color="white")
        mock_img.save.assert_called_once_with(output)

    @patch('generate_qr.qrcode.QRCode')
    def test_generate_vcard_qr(self, mock_qrcode_class):
        mock_qr = mock_qrcode_class.return_value
        mock_img = MagicMock()
        mock_qr.make_image.return_value = mock_img

        name = "John Doe"
        org = "Test Org"
        title = "Dev"
        email = "john@example.com"
        url = "https://example.com"
        output = "test_vcard.png"

        generate_vcard_qr(name, org, title, email, url, output)

        mock_qrcode_class.assert_called_once_with(
            version=1,
            error_correction='L',
            box_size=10,
            border=4,
        )
        # Check that add_data was called with vcard format
        args, kwargs = mock_qr.add_data.call_args
        vcard_data = args[0]
        self.assertIn("BEGIN:VCARD", vcard_data)
        self.assertIn(f"FN:{name}", vcard_data)
        self.assertIn(f"ORG:{org}", vcard_data)
        self.assertIn("END:VCARD", vcard_data)

        mock_qr.make.assert_called_once_with(fit=True)
        mock_qr.make_image.assert_called_once_with(fill_color="black", back_color="white")
        mock_img.save.assert_called_once_with(output)

if __name__ == '__main__':
    unittest.main()
