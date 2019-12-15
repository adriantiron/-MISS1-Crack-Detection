import db


# works with these users in db: admin, user1, user2, user3 and their respective passwords
class TestClass:
    def test_user_type_check(self):
        assert db.user_type_check("admin") == 1
        assert db.user_type_check("user1") == 0
        assert db.user_type_check("user2") == 0
        assert db.user_type_check("user3") == 0
        assert db.user_type_check("mock_user1") == -1
        assert db.user_type_check("mock_user2") == -1
        assert db.user_type_check("mock_user3") == -1

    def test_login_check(self):
        assert db.login_check("mock_user1", "mock_pass1") == -1
        assert db.login_check("mock_user2", "mock_pass2") == -1
        assert db.login_check("mock_user3", "mock_pass3") == -1
        assert db.login_check("user1", "wrong_pass1") == 0
        assert db.login_check("user2", "wrong_pass2") == 0
        assert db.login_check("user3", "wrong_pass3") == 0
        assert db.login_check("admin", "wrong_pass") == 0
        assert db.login_check("user1", "pass1") == 1
        assert db.login_check("user2", "pass2") == 1
        assert db.login_check("user3", "pass3") == 1
        assert db.login_check("admin", "admin") == 1


# terminal command = pytest unit-testing.py

# TODO unit test for uploading test image, check result
