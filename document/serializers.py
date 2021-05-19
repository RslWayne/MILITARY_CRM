from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
import datetime

from major.models import Dossier, Car, Education, Warcraft
from major.services import mailing

from major.serializers import DossierSerializer

from major.services import validated_password


class DocumentSerializer(serializers.ModelSerializer):
    check_date = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Document
        fields = ['id','title','date_expired','date_created','status','document_root','check_date','user']

    def get_check_date(self,obj):
        date_expired = obj.date_expired
        date_now = datetime.datetime.date(timezone.now())
        if date_now > date_expired:
            obj.status = 'dead'
            obj.save()
        return 1

    def create(self, validated_data):
        user = validated_data.pop('user')
        group = user.groups.all()[0].name
        doc_root = validated_data['document_root']
        if group == 'general' and doc_root in ['public','private','secret']:
            document = Document.objects.create(**validated_data)
        elif group == 'president':
            document = Document.objects.create(**validated_data)
        else:
            raise ValidationError('You have no permissions!')
        return document


class RegisterSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=(
        ('common','common'),
        ('warrior','warrior'),

    ),write_only=True)
    dossier = DossierSerializer()

    class Meta:
        model = User
        fields = ['username','email','password','check_password','dossier','user_type']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        dossier_data = validated_data.pop('dossier')
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        user = User.objects.create(**validated_data)

        if password != check_password:
            raise ValidationError("Passwords dont match")
        if not validated_password(password):
            raise ValidationError("Passwords dont match")
        user.set_password(password)
        if user_type == 'warrior':
            user.is_active = False
            group = Group.objects.get(name='serjant')
            user.groups.add(group)
            mailing(user.username)
        user.save()
        cars_data = dossier_data.pop('cars')
        schools_data = dossier_data.pop('schools')
        warcrafts_data = dossier_data.pop('war_crfts')
        dossier = Dossier.objects.create(user=user, **dossier_data)
        for car in cars_data:
            Car.objects.create(dossier=dossier, **car)
        for school in schools_data:
            Education.objects.create(dossier=dossier, **school)
        for wc in warcrafts_data:
            Warcraft.objects.create(dossier=dossier, **wc)
        return user

