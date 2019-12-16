import db, re
from test_network import predict


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
        assert db.login_check("user1", "user1") == 1
        assert db.login_check("user2", "user2") == 1
        assert db.login_check("user3", "user3") == 1
        assert db.login_check("admin", "password") == 1

    def test_nn(self):
        assert predict("not a path") == "File is not image"
        assert predict(r"..\Dataset\Train\Positive\00003.txt") == "File is not image"
        assert self.label(predict(r"..\Dataset\Test\Positive\19003_1.jpg")) == "crack"
        assert self.label(predict(r"..\Dataset\Test\Positive\19380.jpg")) == "crack"
        assert self.label(predict(r"..\Dataset\Test\Positive\19668.jpg")) == "crack"
        assert self.label(predict(r"..\Dataset\Test\Negative\19050.jpg")) == "not crack"
        assert self.label(predict(r"..\Dataset\Test\Negative\19297.jpg")) == "not crack"
        assert self.label(predict(r"..\Dataset\Test\Negative\19621.jpg")) == "not crack"

    def label(self, response):
        return "crack" if int(re.search(r": (\d+)", response).group(1)) >= 50 else "not crack"


# terminal command = pytest unit-testing.py
