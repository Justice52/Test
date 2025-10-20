from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Election, Candidate, Voter, Vote
from .blockchain import blockchain


def home(request):
    """Home page showing active elections"""
    elections = Election.objects.filter(is_active=True)
    context = {
        'elections': elections,
    }
    return render(request, 'voting/home.html', context)


def election_list(request):
    """List all elections"""
    elections = Election.objects.all()
    context = {
        'elections': elections,
    }
    return render(request, 'voting/election_list.html', context)


def election_detail(request, election_id):
    """Show election details and candidates"""
    election = get_object_or_404(Election, id=election_id)
    candidates = election.candidates.all()
    
    # Get vote counts from blockchain
    for candidate in candidates:
        candidate.vote_count = candidate.get_vote_count()
    
    context = {
        'election': election,
        'candidates': candidates,
        'is_ongoing': election.is_ongoing(),
    }
    return render(request, 'voting/election_detail.html', context)


@login_required
def vote(request, election_id):
    """Cast a vote"""
    election = get_object_or_404(Election, id=election_id)
    
    # Check if election is ongoing
    if not election.is_ongoing():
        messages.error(request, 'This election is not currently active.')
        return redirect('election_detail', election_id=election_id)
    
    # Get or create voter
    try:
        voter = Voter.objects.get(user=request.user)
    except Voter.DoesNotExist:
        messages.error(request, 'You are not registered as a voter.')
        return redirect('election_detail', election_id=election_id)
    
    # Check if already voted
    if Vote.objects.filter(voter=voter, election=election).exists():
        messages.error(request, 'You have already voted in this election.')
        return redirect('election_detail', election_id=election_id)
    
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        if not candidate_id:
            messages.error(request, 'Please select a candidate.')
            return redirect('vote', election_id=election_id)
        
        candidate = get_object_or_404(Candidate, id=candidate_id, election=election)
        
        # Add vote to blockchain
        vote_data = {
            'voter_id': voter.id,
            'candidate_id': candidate.id,
            'election_id': election.id,
            'timestamp': str(timezone.now())
        }
        
        block = blockchain.add_block(vote_data)
        
        # Save vote record in database
        vote_record = Vote.objects.create(
            voter=voter,
            candidate=candidate,
            election=election,
            blockchain_hash=block.hash
        )
        
        # Mark voter as voted
        voter.has_voted = True
        voter.save()
        
        messages.success(request, f'Your vote for {candidate.name} has been recorded successfully!')
        return redirect('vote_confirmation', vote_id=vote_record.id)
    
    candidates = election.candidates.all()
    context = {
        'election': election,
        'candidates': candidates,
    }
    return render(request, 'voting/vote.html', context)


@login_required
def vote_confirmation(request, vote_id):
    """Show vote confirmation"""
    vote = get_object_or_404(Vote, id=vote_id)
    
    # Ensure the vote belongs to the current user
    if vote.voter.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {
        'vote': vote,
    }
    return render(request, 'voting/vote_confirmation.html', context)


def blockchain_view(request):
    """View the blockchain"""
    chain = blockchain.get_chain()
    is_valid = blockchain.is_chain_valid()
    
    context = {
        'chain': chain,
        'is_valid': is_valid,
        'chain_length': len(chain),
    }
    return render(request, 'voting/blockchain.html', context)


def results(request, election_id):
    """Show election results"""
    election = get_object_or_404(Election, id=election_id)
    candidates = election.candidates.all()
    
    # Get vote counts from blockchain
    results_data = []
    total_votes = 0
    for candidate in candidates:
        vote_count = candidate.get_vote_count()
        total_votes += vote_count
        results_data.append({
            'candidate': candidate,
            'votes': vote_count,
        })
    
    # Calculate percentages
    for result in results_data:
        if total_votes > 0:
            result['percentage'] = (result['votes'] / total_votes) * 100
        else:
            result['percentage'] = 0
    
    # Sort by votes (descending)
    results_data.sort(key=lambda x: x['votes'], reverse=True)
    
    context = {
        'election': election,
        'results': results_data,
        'total_votes': total_votes,
    }
    return render(request, 'voting/results.html', context)
