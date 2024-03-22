from django.db import models
from djongo.models.fields import EmbeddedField, ObjectIdField

class SiteInfo(models.Model):
    _id = ObjectIdField()
    site_title = models.CharField(max_length=100)

class TrafficEngagementInfo(models.Model):
    _id = ObjectIdField()
    total_visits = models.CharField(max_length=10)
    bounce_rate = models.CharField(max_length=10)
    pages_per_visit = models.CharField(max_length=10)
    average_visit_duration = models.CharField(max_length=10)
    last_month_changes = models.CharField(max_length=10)

class CountryClassification(models.Model):
    _id = ObjectIdField()
    classification = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

class CategoryClassification(models.Model):
    _id = ObjectIdField()
    classification = models.CharField(max_length=10)
    category = models.CharField(max_length=100)

class KeywordInfo(models.Model):
    _id = ObjectIdField()
    keyword = models.CharField(max_length=100)
    access_by_keyword = models.CharField(max_length=10)

class GenderTrafficInfo(models.Model):
    _id = ObjectIdField()
    gender = models.CharField(max_length=20)
    percentage = models.CharField(max_length=10)

class AgeTrafficInfo(models.Model):
    _id = ObjectIdField()
    type = models.CharField(max_length=20)
    percentage = models.CharField(max_length=10)

class SocialMediaTrafficInfo(models.Model):
    _id = ObjectIdField()
    type = models.CharField(max_length=50)
    percentage = models.CharField(max_length=10)

class OriginTrafficInfo(models.Model):
    _id = ObjectIdField()
    type = models.CharField(max_length=20)
    percentage = models.CharField(max_length=10)

class CountryInfo(models.Model):
    _id = ObjectIdField()
    country = models.CharField(max_length=100)
    percentage = models.CharField(max_length=10)

class CountryTrafficInfo(models.Model):
    _id = ObjectIdField()
    country_1 = EmbeddedField(model_container=CountryInfo)
    country_2 = EmbeddedField(model_container=CountryInfo)
    country_3 = EmbeddedField(model_container=CountryInfo)
    country_4 = EmbeddedField(model_container=CountryInfo)
    country_5 = EmbeddedField(model_container=CountryInfo)
    country_6 = EmbeddedField(model_container=CountryInfo)

class TrafficSourceInfo(models.Model):
    _id = ObjectIdField()
    type = models.CharField(max_length=50)
    percentage = models.CharField(max_length=10)


class CompetidorAux(models.Model):
    _id = ObjectIdField()
    site = models.CharField(max_length=100)
    monthly_views = models.CharField(max_length=100)
    ranking = models.CharField(max_length=100)

class CompetitorInfo(models.Model):
    _id = ObjectIdField()
    place_1 = EmbeddedField(model_container=CompetidorAux)
    place_2 = EmbeddedField(model_container=CompetidorAux)
    place_3 = EmbeddedField(model_container=CompetidorAux)
    place_4 = EmbeddedField(model_container=CompetidorAux)
    place_5 = EmbeddedField(model_container=CompetidorAux)
    place_6 = EmbeddedField(model_container=CompetidorAux)
    place_7 = EmbeddedField(model_container=CompetidorAux)
    place_8 = EmbeddedField(model_container=CompetidorAux)
    place_9 = EmbeddedField(model_container=CompetidorAux)
    place_10 = EmbeddedField(model_container=CompetidorAux)

class TargetAudienceInfo(models.Model):
    _id = ObjectIdField()
    target_audience = models.CharField(max_length=100)
    main_topics = models.CharField(max_length=100)

class Data(models.Model):
    _id = ObjectIdField()
    site_info = EmbeddedField(model_container=SiteInfo)
    traffic_engagement_info = EmbeddedField(model_container=TrafficEngagementInfo)
    keywords_info = EmbeddedField(model_container=KeywordInfo)
    traffic_by_gender_info = EmbeddedField(model_container=GenderTrafficInfo)
    traffic_by_age_info = EmbeddedField(model_container=AgeTrafficInfo)
    traffic_by_social_media_info = EmbeddedField(model_container=SocialMediaTrafficInfo)
    origin_traffic_info = EmbeddedField(model_container=OriginTrafficInfo)
    traffic_by_country_info = EmbeddedField(model_container=CountryTrafficInfo)
    traffic_sources_info = EmbeddedField(model_container=TrafficSourceInfo)
    competitors_info = EmbeddedField(model_container=CompetitorInfo)
    target_audience_info = EmbeddedField(model_container=TargetAudienceInfo)
