"""
Script to populate the database with sample election data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evoting_system.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from voting.models import Election, Candidate, Voter

# Create sample election
election = Election.objects.create(
    title="Student Council President Election 2025",
    description="Vote for your next student council president. This election will determine who will lead the student body for the upcoming academic year.",
    start_date=timezone.now() - timedelta(hours=1),
    end_date=timezone.now() + timedelta(days=7),
    is_active=True
)

# Create candidates
candidates_data = [
    {
        'name': 'Alice Johnson',
        'description': 'Experienced leader with a vision for innovation and student engagement. Former class president with proven track record.',
    },
    {
        'name': 'Bob Smith',
        'description': 'Advocate for student rights and campus improvement. Committed to making positive changes in our community.',
    },
    {
        'name': 'Carol Williams',
        'description': 'Passionate about sustainability and inclusive campus culture. Fresh perspectives for modern challenges.',
    },
]

for candidate_data in candidates_data:
    Candidate.objects.create(
        election=election,
        **candidate_data
    )

# Create sample voters
print("Creating sample voters...")
for i in range(1, 6):
    username = f'voter{i}'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=f'voter{i}@example.com',
            password='voter123',
            first_name=f'Voter',
            last_name=str(i)
        )
        
        Voter.objects.create(
            user=user,
            voter_id=f'V{1000 + i}'
        )
        print(f'Created voter: {username} (password: voter123)')

print("\n✓ Sample data created successfully!")
print(f"\nElection: {election.title}")
print(f"Candidates: {election.candidates.count()}")
print(f"Voters registered: {Voter.objects.count()}")
print("\nYou can now:")
print("1. Login as admin (username: admin, password: admin123)")
print("2. Login as any voter (username: voter1-5, password: voter123)")
print("3. Cast votes and view results on the blockchain")
