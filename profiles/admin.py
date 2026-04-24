from django.contrib import admin
from .models import InnovatorProfile, StartupProfile, InvestorProfile, ConsultantProfile, EcosystemPartnerProfile

for model in [InnovatorProfile, StartupProfile, InvestorProfile, ConsultantProfile, EcosystemPartnerProfile]:
    admin.site.register(model)
