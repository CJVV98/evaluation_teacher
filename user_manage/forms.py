class UserData:
    user_data = None

    @classmethod
    def set_user_data(cls, value):
        cls.user_data = value

    @classmethod
    def get_user_data(cls):
        return cls.user_data