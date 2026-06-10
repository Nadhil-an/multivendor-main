from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserManagerTests(TestCase):
    
    def test_create_user(self):
        """Test creating a normal user with valid credentials."""
        user = User.objects.create_user(
            email='normal@user.com',
            username='normaluser',
            first_name='Normal',
            last_name='User',
            password='foo'
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.username, 'normaluser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superadmin)

    def test_create_superuser(self):
        """Test creating a superuser with valid credentials."""
        admin_user = User.objects.create_superuser(
            email='super@user.com',
            username='superuser',
            first_name='Super',
            last_name='User',
            password='foo'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'superuser')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superadmin)

    def test_create_user_no_email(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaisesMessage(ValueError, "User must have a email address"):
            User.objects.create_user(
                email='',
                username='nouseremail',
                first_name='No',
                last_name='Email',
                password='foo'
            )

    def test_create_user_no_username(self):
        """Test that creating a user without a username raises a ValueError."""
        with self.assertRaisesMessage(ValueError, "User must have a username"):
            User.objects.create_user(
                email='nousername@user.com',
                username='',
                first_name='No',
                last_name='Username',
                password='foo'
            )

    def test_user_get_role(self):
        """Test the get_role method of the User model."""
        restaurant_user = User(role=User.RESTAURANT)
        customer_user = User(role=User.CUSTOMER)
        other_user = User(role=None)

        self.assertEqual(restaurant_user.get_role(), "Vendor")
        self.assertEqual(customer_user.get_role(), "Customer")
        self.assertEqual(other_user.get_role(), "")
