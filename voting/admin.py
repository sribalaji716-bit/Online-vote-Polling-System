from django.contrib import admin
from .models import Voter, Position, Candidate, Votes


admin.site.register(Voter)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Votes)
