"""
Blockchain implementation for secure vote storage
"""
import hashlib
import json
from time import time
from typing import List, Dict, Any


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Blockchain for storing votes securely"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 2  # Number of leading zeros required in hash
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(0, time(), {'vote': 'Genesis Block'}, '0')
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_block(self, data: Dict[str, Any]) -> Block:
        """Add a new block to the blockchain with proof of work"""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time(),
            data=data,
            previous_hash=previous_block.hash
        )
        
        # Proof of work
        new_block = self.proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block
    
    def proof_of_work(self, block: Block) -> Block:
        """
        Simple proof of work algorithm:
        - Find a number (nonce) such that hash(block) contains leading zeros
        """
        block.nonce = 0
        block.hash = block.calculate_hash()
        
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        
        return block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if not current_block.hash.startswith('0' * self.difficulty):
                return False
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the entire blockchain as a list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_votes_for_candidate(self, candidate_id: int) -> int:
        """Count votes for a specific candidate from the blockchain"""
        count = 0
        for block in self.chain[1:]:  # Skip genesis block
            if block.data.get('candidate_id') == candidate_id:
                count += 1
        return count
    
    def verify_vote(self, voter_id: int) -> bool:
        """Check if a voter has already voted"""
        for block in self.chain[1:]:  # Skip genesis block
            if block.data.get('voter_id') == voter_id:
                return True
        return False


# Global blockchain instance
blockchain = Blockchain()
