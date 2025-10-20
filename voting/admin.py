from django.contrib import admin
from .models import Election, Candidate, Voter, Vote


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active', 'is_ongoing']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'election', 'get_vote_count']
    list_filter = ['election']
    search_fields = ['name', 'description']


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['voter_id', 'user', 'has_voted', 'registered_at']
    list_filter = ['has_voted', 'registered_at']
    search_fields = ['voter_id', 'user__username', 'user__email']
    readonly_fields = ['registered_at']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'election', 'timestamp', 'blockchain_hash']
    list_filter = ['election', 'timestamp']
    search_fields = ['voter__voter_id', 'blockchain_hash']
    readonly_fields = ['timestamp', 'blockchain_hash']
    
    def has_add_permission(self, request):
        # Prevent manual vote creation through admin
        return False
    
    def has_change_permission(self, request, obj=None):
        # Prevent vote modification
        return False
