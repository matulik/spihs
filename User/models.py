# coding=UTF-8

# Session timeout variable
sessionTimeout = 10000

from django.db import models
from hashlib import sha1
from django.core.validators import EmailValidator

class User(models.Model):
    username = models.CharField(max_length=20, blank=False, unique=True, verbose_name=u"Login")
    password = models.CharField(max_length=100, blank=False, unique=True, verbose_name=u"Password")
    email = models.EmailField(blank=False, verbose_name="E-mail")
    status = models.IntegerField(blank=False, default=0)

    def save(self, *args, **kwargs):
        self.password = self.passwordAsSHA1(self.password)
        if self.status <-1 and self.status > 4:
            self.status = 0
        super(User, self).save(*args, **kwargs)

    def saveUserObject(self, username, password, email):
        if self.validate(username, password, email):
            self.username = username
            self.password = self.passwordAsSHA1(password)
            self.email = email
            self.status = 0
            self.save()
            print u"User added"

    def passwordAsSHA1(self, password):
        return sha1(str(password)).hexdigest()

    def validate(self, login, password, email):
        # Method to validate data before save model
        ret = True
        logstring = u""
        if len(str(login)) <3 and len(str(login)) >=20:
            ret = False
            logstring += u"Bad login length\n"
        if len(str(password)) <3 and len(str(password)) >=20:
            ret = False
            logstring += u"Bad password length\n"
        if False: ## Email Validation
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
        return True

    def logout(self, request):
        request.session.flush()
        request.session['login'] = False
        request.session['id'] = None

    def userAuth(self, request):
        if not request.session.get('login', None):
            return False
        elif request.session['login'] == True:
            uid = request.session['id']
            if User.objects.filter(id=uid).exists():
                user = User.objects.get(id=uid)
                if user.status >= 0:
                    return True
        return False