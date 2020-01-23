from party import Party
import unittest

PARTY_NAME = 'Test_Party'
USERNAME =  'Test_User'
PLAYLIST_ID = 123
AUTHORIZATION_CODE = 456;


class PartyTest(unittest.TestCase):
    @classmethod
    def  setUp(self):
        self.party = Party(PARTY_NAME, USERNAME, AUTHORIZATION_CODE)

    def test_user_true(self):
        self.assertEqual(self.party.user, USERNAME)

    def test_user_false(self):
        self.assertNotEqual(self.party.user, 'not_a_username')

    def test_party_name_true(self):
        self.assertEqual(self.party.party_name, PARTY_NAME)

    def test_party_name_false(self):
        self.assertNotEqual(self.party.party_name, 'not_a_party')

    def test_auth_code_true(self):
        self.assertEqual(self.party.auth_code, AUTHORIZATION_CODE)

    def test_auth_code_false(self):
        self.assertNotEqual(self.party.auth_code, 'not_auth_code')

    @classmethod
    def teardown(self):
        self.party.destroy()


