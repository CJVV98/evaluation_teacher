from django.test import TestCase
from user_manage.models import User
from datetime import datetime
# Create your tests here.


class UserTest(TestCase):
    
      def test_register_user(self):
        # Crea un objeto BlogPost
        new_user = User(
            user="MARTHA",
            password="Master01*",
            pub_date=datetime.now()
        )

        # Guarda el objeto en la base de datos de MongoDB
        new_user.save()

        # Recupera el objeto de la base de datos
        retrieved_user = User.objects.get( user="MARTHA")

        # Asegúrate de que los datos guardados sean correctos
        self.assertEqual(retrieved_user.user, "MARTHA")
        self.assertEqual(retrieved_user.password, "Master01*")
