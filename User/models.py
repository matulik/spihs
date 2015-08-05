# coding=UTF-8

# Session timeout variable
sessionTimeout = 500
defaulTokenString = u'logout'

from django.db import models
from hashlib import sha1, md5
from django.core.validators import EmailValidator

# For token generator
from string import ascii_uppercase
from random import choice
from django.utils import timezone


def defaultToken():
    md5token = (md5(defaulTokenString)).hexdigest()
    return md5token


class Token(models.Model):
    token = models.CharField(max_length=32, blank=False, default=defaultToken)
    dateCreate = models.DateTimeField(default=timezone.now())

    def generateToken(self):
        token = (''.join(choice(ascii_uppercase) for i in range(32)))
        md5token = (md5(token)).hexdigest()
        self.dateCreate = timezone.now()
        return md5token

    def compareTokens(self, token):
        if token == self.token:
            return True
        else:
            return False


class User(models.Model):
    username = models.CharField(max_length=20, blank=False, unique=True, verbose_name=u"Login")
    password = models.CharField(max_length=100, blank=False, unique=True, verbose_name=u"Password")
    email = models.EmailField(blank=False, verbose_name="E-mail")
    status = models.IntegerField(blank=False, default=0)
    token = models.ForeignKey(Token, related_name='token_md5')

    def createNewToken(self):
        token = Token()
        token.save()
        return token

    def save(self, *args, **kwargs):
        # Cheking if not null
        if not self.password:
            self.password = self.passwordAsSHA1(self.password)
        if not self.token:
            self.token = self.createNewToken()
        if self.status < -1 and self.status > 4:
            self.status = 0
        super(User, self).save(*args, **kwargs)

    def saveUserObject(self, username, password, email):
        if self.validate(username, password, email):
            self.username = username
            self.password = self.passwordAsSHA1(password)
            self.email = email
            self.status = 0
            self.token = self.createNewToken()
            self.save()
            print u"User added"

    def passwordCompare(self, password):
        if self.password == self.passwordAsSHA1(password):
            return True
        else:
            return False

    def passwordAsSHA1(self, password):
        return sha1(password).hexdigest()

    def validate(self, login, password, email):
        # Method to validate data before save model
        ret = True
        logstring = u""
        if len(str(login)) < 3 and len(str(login)) >= 20:
            ret = False
            logstring += u"Bad login length\n"
        if len(str(password)) < 3 and len(str(password)) >= 20:
            ret = False
            logstring += u"Bad password length\n"
        if False:  ## Email Validation
            ret = False
            logstring += u"Bad email address\n"
        if ret:
            print u"Validation ok"
        else:
            print logstring
        return ret

    def login(self, request):
        request.session['login'] = True
        request.session['id'] = self.id
        request.session.set_expiry(sessionTimeout)
        # Set new token
        token = Token.objects.get(id=self.token_id)
        token.token = token.generateToken()
        token.save()
        request.session['token'] = self.token.token
        # Set model status
        self.status = 1
        self.save()
        print u'Login ' + self.username + ' successfully with token ' + self.token.token
        return True

    def logout(self, request):
        request.session.flush()
        request.session['login'] = False
        request.session['id'] = None
        request.session['token'] = None
        # Set default token
        token = Token.objects.get(id=self.token_id)
        token.token = defaultToken()
        token.save()
        # Set model status
        self.status = 0
        self.save()

    @staticmethod
    def getUserToken(id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            print 'Token for user doesnt exist'
            return None
        return user.token.token

    @staticmethod
    def userAuth(request, tokkening):
        if not request.session.get('login', None):
            return False
        elif request.session['login'] == True:
            if tokkening == True:
                if str(request.session['token']) != str(User.getUserToken(request.session['id'])):
                    return False
            uid = request.session['id']
            if User.objects.filter(id=uid).exists():
                user = User.objects.get(id=uid)
                if user.status >= 0:
                    return True
        return False
