from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from .services import mailing


class CarSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Car
        fields = ['id','mark','year','number','color','type']


class EducationSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()


    class Meta:
        model = Education
        fields = ['id','start_date','end_date','school_name','major']



class WarcraftSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Warcraft
        fields = ['id','military_area','start_date','end_date','military_area','major']


class DossierSerializer(serializers.ModelSerializer):
    cars = CarSerializers(many=True)
    schools = EducationSerializers(many=True)
    war_crfts = WarcraftSerializers(many=True)

    class Meta:
        model = Dossier
        fields = ['id','full_name','image', 'date_birth','cars','schools','war_crfts']

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        cars_data = validated_data.pop('cars')
        schools_data = validated_data.pop('schools')
        warcrafts_data = validated_data.pop('war_crafts')
        ids_list_car = [car.id for car in instance.car.all()]
        current_ids_car = [car['id'] for car in cars_data]
        final_list_car = [car_id for car_id in ids_list_car if car_id not in current_ids_car]
        for car in cars_data:
            car_id = car['id']
            car_data = Car.objects.get(id=car_id)
            for delete_id in final_list_car:
                delete_car = Car.objects.get(id=delete_id)
                delete_car.delete()
            car_data.mark = car['mark']
            car_data.model = car['model']
            car_data.year = car['year']
            car_data.number = car['number']
            car_data.color = car['color']
            car_data.type = car['type']
            car_data.save()
            ids_list_school = [schools.id for schools in instance.school.all()]
            current_ids_school = [school['id'] for school in schools_data]
            final_list_school = [school_id for school_id in ids_list_school if school_id not in current_ids_school]
        for school in schools_data:
            school_id = school['id']
            school_data = Education.objects.get(id=school_id)
            for delete_id in final_list_school:
                delete_car = Education.objects.get(id=delete_id)
                delete_car.delete()
            school_data.school_name = school['school_name']
            school_data.start_date = school['start_date']
            school_data.end_date = school['end_date']
            school_data.major = school['major']
            school_data.save()
            ids_list_warcraft = [warcrafts.id for warcrafts in instance.warcraft.all()]
            current_ids_warcraft = [warcrafts['id'] for warcrafts in warcrafts_data]
            final_list_warcrafts = [warcrafts_id for warcrafts_id in ids_list_warcraft if warcrafts_id not in current_ids_warcraft]
        for warcrafts in warcrafts_data:
            warcrafts_id = warcrafts['id']
            warcrafts_data = Warcraft.objects.get(id=warcrafts_id)
            for delete_id in final_list_warcrafts:
                delete_warcraft = Warcraft.objecst.get(id=delete_id)
                delete_warcraft.delete()
            warcrafts_data.military_area = warcrafts['military_area']
            warcrafts_data.start_date = warcrafts['start_date']
            warcrafts_data.end_date = warcrafts['end_date']
            warcrafts_data.major = warcrafts['major']
            warcrafts_data.start_pose = warcrafts['start_pose']
            warcrafts_data.end_pose = warcrafts['end_pose']
            warcrafts_data.save()
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)

    dossier = DossierSerializer()


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'check_password', 'dossier']


    @transaction.atomic
    def create(self, validated_data):

        dossier_data = validated_data.pop('dossier')
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        user = User.objects.create(**validated_data)
        if password != check_password:
            raise ValidationError("Passwords don't match")
        user.set_password(password)
        user.is_active = False
        group = Group.objects.get(name='sergeant')
        user.groups.add(group)
        mailing(user.username)
        user.save()
        cars_data = dossier_data.pop('cars')
        schools_data = dossier_data.pop('schools')
        war_data = dossier_data.pop('war_crfts')
        dossier = Dossier.objects.create(user=user, **dossier_data)

        for car in cars_data:
            Car.objects.create(dossier=dossier, **car)

        for school in schools_data:
            Education.objects.create(dossier=dossier, **school)

        for war in war_data:
            Warcraft.objects.create(dossier=dossier, **war)
        return user


