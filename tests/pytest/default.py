import unittest
import os
import pathlib
import bcrypt
from utils.common import read_yaml, validate_username, get_hashed_password


class TestCommonUtils(unittest.TestCase):

    def test_read_yaml(self):
        self.assertEqual(read_yaml(os.path.join(pathlib.Path().resolve(
        ), "tests/test.yaml")), {"UNIT_TESTING": {"DUMMY": "dummy_value"}})

    def test_validate_username(self):
        self.assertTrue(validate_username("jane.doe@gmail.com"))
        self.assertTrue(validate_username("jane.doe@gmail.co.uk"))
        self.assertFalse(validate_username("jane.doe"))

    def test_hashedPassword(self):
        password = "$ecret@123"
        hashed_pwd = get_hashed_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_pwd))

if __name__ == '__main__':
    unittest.main()
