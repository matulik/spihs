# coding=UTF-8

# Session timeout variable
sessionTimeout = 10000

from django.db import models
from hashlib import sha1
from django.core.validators import EmailValidator

class User(models.Model):
    login = models.CharField(max_length=20, blank=False, unique=True, verbose_name=u"Login")
    password = models.CharField(blank=False, unique=True, verbose_name=u"Password")
    email = models.EmailField(blank=False, verbose_name="E-mail")
    status = models.IntegerField(blank=False, default=0)

    def __init__(self):
        print "Init"
        ### TODO ###

    def passwordAsSHA1(password):
        return sha1(str(password)).hexdigest()

    def validate(login, password, email):
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