from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class userManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("User must have a email address")
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email      = self.normalize_email(email),
            username   = username,
            first_name = first_name,
            last_name  = last_name,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,first_name,last_name,username,email,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin  = True
        user.is_active = True
        user.is_staff  = True
        user.is_superadmin = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    
    RESTAURANT = 1
    CUSTOMER   = 2 

    ROLE_CHOICE = [
        (RESTAURANT,'Restaurant'),
        (CUSTOMER,'customer')
    ]

    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    username   = models.CharField(max_length=50)
    email      = models.EmailField(max_length=100,unique=True)
    phone_number     = models.CharField(max_length=50)
    role       = models.PositiveBigIntegerField(choices = ROLE_CHOICE, blank=True,null=True)


    #required fileds

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = userManager() 

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None): 
        return self.is_admin
    def has_module_perms(self, app_label):  
        return True
    def get_role(self):
        if self.role == self.RESTAURANT:
            return "Vendor"
        elif self.role == self.CUSTOMER:
            return "Customer"
        return ""
 


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True )
    cover_photo = models.ImageField(upload_to='users/cover_photos/',blank=True,null=True )
    address = models.CharField(max_length=250,blank=True,null=True)
    
    country = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    city  = models.CharField(max_length=50,blank=True,null=True)
    pin_code = models.CharField(max_length=30,blank=True,null=True)
    
    longitude = models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    latitude = models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    place_id = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    

    

    def __str__(self):
        return self.user.email
    

    def __str__(self):
        return self.name or self.address or self.place_id
    
    cover_photo = models.ImageField(upload_to='users/cover_photos/',blank=True,null=True,default='/images/cover-photo-1.PNG' )
    
    
