from django.test import TestCase
from django.contrib.auth.models import User
from render import UserRender, UserRenderTwo


class UserRenderTest(TestCase):
    def test_rendering(self):
        user, created = User.objects.get_or_create(username='user')
        user.set_password('user')
        user.save()

        sample_data = {
            'username': 'kuba',
            'cos' : 'cos_value',
            }

        render = UserRenderTwo(user)
        print str(render)
