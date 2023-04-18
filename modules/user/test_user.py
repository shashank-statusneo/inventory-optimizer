from json import dumps


def register_new_user(self):
    return self.client.post(
        "/starter-kit/user/",
        data=dumps(
            dict(
                email="example@gmail.com",
                username="username",
                password="password",
            )
        ),
        content_type="application/json",
    )
