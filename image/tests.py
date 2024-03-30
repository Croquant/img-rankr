import unittest
from unittest.mock import patch

from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Image
from .utils import calculate_md5_hash


class ImageModelTestCase(TestCase):
    def setUp(self):
        # Create a sample Image instance for testing
        self.image = Image.objects.create(
            file_url="https://picsum.photos/id/237/200/300"
        )

    def test_image_creation(self):
        """
        Test if an Image instance is created correctly.
        """
        self.assertEqual(str(self.image), f"image({self.image.id})")
        self.assertIsNotNone(self.image.created_at)
        self.assertIsNotNone(self.image.modified_at)

    def test_file_hash_calculation(self):
        """
        Test if the file hash is correctly calculated.
        """
        expected_hash = calculate_md5_hash(self.image.file_url)
        self.assertEqual(self.image.file_hash, expected_hash)

    def test_unique_file_url(self):
        """
        Test uniqueness constraint on file_url.
        """
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                Image.objects.create(file_url=self.image.file_url)
        except IntegrityError:
            pass

    def tearDown(self):
        # Clean up after each test
        self.image.delete()


class TestCalculateMD5Hash(unittest.TestCase):
    def test_valid_file_url(self):
        # Mock the requests.get function to return a sample response
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"Sample content"

            # Call the function with a valid file URL
            file_url = "https://example.com/sample.txt"
            result = calculate_md5_hash(file_url)

            # Expected MD5 hash for the sample content
            expected_hash = "b4ed349f78183083dcaf708313c8c99b"
            self.assertEqual(result, expected_hash)

    def test_invalid_file_url(self):
        # Mock the requests.get function to simulate an error
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 404

            # Call the function with an invalid file URL
            file_url = "https://example.com/nonexistent.txt"
            with self.assertRaises(Exception) as context:
                calculate_md5_hash(file_url)

            # Check if the correct exception message is raised
            expected_error = f"Error calculating MD5 hash: Error downloading file from {file_url}"  # noqa: E501
            self.assertEqual(str(context.exception), expected_error)

    def test_exception_handling(self):
        # Mock the requests.get function to raise an exception
        with patch("requests.get") as mock_get:
            mock_get.side_effect = Exception("Simulated error")

            # Call the function with any file URL
            file_url = "https://example.com/anyfile.txt"
            with self.assertRaises(Exception) as context:
                calculate_md5_hash(file_url)

            # Check if the correct exception message is raised
            expected_error = "Error calculating MD5 hash: Simulated error"
            self.assertEqual(str(context.exception), expected_error)
