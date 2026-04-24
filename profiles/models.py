from django.db import models
from django.conf import settings


class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class InnovatorProfile(BaseProfile):
    skills = models.JSONField(default=list, blank=True)
    areas_of_interest = models.JSONField(default=list, blank=True)
    stage = models.CharField(max_length=100, blank=True, help_text='e.g., Idea, Prototype')
    looking_for = models.JSONField(default=list, blank=True, help_text='e.g., Co-founder, Funding')

    def __str__(self):
        return f'Innovator: {self.user.full_name}'


class StartupProfile(BaseProfile):
    company_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=100, blank=True, help_text='e.g., Pre-seed, Seed, Series A')
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    team_size = models.PositiveIntegerField(null=True, blank=True)
    funding_raised = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    problem_statement = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    target_market = models.TextField(blank=True)
    pitch_deck_url = models.URLField(blank=True)
    looking_for = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'Startup: {self.company_name}'


class InvestorProfile(BaseProfile):
    firm_name = models.CharField(max_length=200, blank=True)
    investment_thesis = models.TextField(blank=True)
    sectors_of_interest = models.JSONField(default=list, blank=True)
    investment_stages = models.JSONField(default=list, blank=True)
    ticket_size_min = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ticket_size_max = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    portfolio_companies = models.JSONField(default=list, blank=True)
    total_investments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Investor: {self.user.full_name}'


class ConsultantProfile(BaseProfile):
    expertise = models.JSONField(default=list, blank=True)
    industries_served = models.JSONField(default=list, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    services_offered = models.JSONField(default=list, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.CharField(max_length=100, blank=True, help_text='e.g., Part-time, Full-time')
    certifications = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'Consultant: {self.user.full_name}'


class EcosystemPartnerProfile(BaseProfile):
    organization_name = models.CharField(max_length=200)
    organization_type = models.CharField(
        max_length=50,
        choices=[
            ('accelerator', 'Accelerator'),
            ('incubator', 'Incubator'),
            ('vc_fund', 'VC Fund'),
            ('angel_network', 'Angel Network'),
            ('corporate', 'Corporate Innovation'),
            ('government', 'Government Body'),
            ('university', 'University/Research'),
            ('ngo', 'NGO'),
            ('other', 'Other'),
        ]
    )
    programs_offered = models.JSONField(default=list, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    cohort_size = models.PositiveIntegerField(null=True, blank=True)
    equity_taken = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='%')
    funding_provided = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sectors_focus = models.JSONField(default=list, blank=True)
    stage_focus = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'Ecosystem Partner: {self.organization_name}'
