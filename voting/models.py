from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Election(models.Model):
    """Represents an election event"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def is_ongoing(self):
        """Check if election is currently ongoing"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
    
    class Meta:
        ordering = ['-created_at']


class Candidate(models.Model):
    """Represents a candidate in an election"""
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.CharField(max_length=500, blank=True, help_text="URL to candidate photo")
    
    def __str__(self):
        return f"{self.name} - {self.election.title}"
    
    def get_vote_count(self):
        """Get vote count from blockchain"""
        from .blockchain import blockchain
        return blockchain.get_votes_for_candidate(self.id)
    
    class Meta:
        ordering = ['name']


class Voter(models.Model):
    """Represents a registered voter"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=50, unique=True)
    has_voted = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.voter_id})"
    
    def has_voted_in_blockchain(self):
        """Verify if voter has voted by checking blockchain"""
        from .blockchain import blockchain
        return blockchain.verify_vote(self.id)
    
    class Meta:
        ordering = ['voter_id']


class Vote(models.Model):
    """
    Represents a vote record (stored in database for quick reference)
    The actual vote is stored in the blockchain for immutability
    """
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    blockchain_hash = models.CharField(max_length=64)
    
    def __str__(self):
        return f"Vote by {self.voter.voter_id} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        # Ensure one vote per voter per election
        unique_together = ['voter', 'election']
