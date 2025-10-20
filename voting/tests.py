"""
Tests for the blockchain implementation
"""
from django.test import TestCase
from voting.blockchain import Block, Blockchain
from time import time


class BlockTestCase(TestCase):
    """Test cases for Block class"""
    
    def test_block_creation(self):
        """Test that a block can be created"""
        block = Block(
            index=0,
            timestamp=time(),
            data={'test': 'data'},
            previous_hash='0'
        )
        self.assertIsNotNone(block.hash)
        self.assertEqual(block.index, 0)
    
    def test_block_hash_calculation(self):
        """Test that block hash is calculated correctly"""
        block = Block(
            index=0,
            timestamp=time(),
            data={'test': 'data'},
            previous_hash='0'
        )
        calculated_hash = block.calculate_hash()
        self.assertEqual(block.hash, calculated_hash)
    
    def test_block_to_dict(self):
        """Test block serialization to dictionary"""
        block = Block(
            index=0,
            timestamp=time(),
            data={'test': 'data'},
            previous_hash='0'
        )
        block_dict = block.to_dict()
        self.assertIn('index', block_dict)
        self.assertIn('hash', block_dict)
        self.assertIn('data', block_dict)


class BlockchainTestCase(TestCase):
    """Test cases for Blockchain class"""
    
    def setUp(self):
        """Set up a new blockchain for each test"""
        self.blockchain = Blockchain()
    
    def test_genesis_block_creation(self):
        """Test that genesis block is created"""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].previous_hash, '0')
    
    def test_add_block(self):
        """Test adding a new block to the blockchain"""
        initial_length = len(self.blockchain.chain)
        vote_data = {
            'voter_id': 1,
            'candidate_id': 2,
            'election_id': 1
        }
        block = self.blockchain.add_block(vote_data)
        
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        self.assertEqual(block.data, vote_data)
        self.assertTrue(block.hash.startswith('0' * self.blockchain.difficulty))
    
    def test_chain_validity(self):
        """Test blockchain validation"""
        # Add some blocks
        self.blockchain.add_block({'voter_id': 1, 'candidate_id': 1})
        self.blockchain.add_block({'voter_id': 2, 'candidate_id': 2})
        
        # Chain should be valid
        self.assertTrue(self.blockchain.is_chain_valid())
    
    def test_chain_invalidity_on_tampering(self):
        """Test that tampering is detected"""
        # Add a block
        self.blockchain.add_block({'voter_id': 1, 'candidate_id': 1})
        
        # Tamper with the data
        self.blockchain.chain[1].data = {'voter_id': 999, 'candidate_id': 999}
        
        # Chain should now be invalid
        self.assertFalse(self.blockchain.is_chain_valid())
    
    def test_get_votes_for_candidate(self):
        """Test counting votes for a candidate"""
        # Add votes for different candidates
        self.blockchain.add_block({'voter_id': 1, 'candidate_id': 1})
        self.blockchain.add_block({'voter_id': 2, 'candidate_id': 1})
        self.blockchain.add_block({'voter_id': 3, 'candidate_id': 2})
        
        # Check vote counts
        self.assertEqual(self.blockchain.get_votes_for_candidate(1), 2)
        self.assertEqual(self.blockchain.get_votes_for_candidate(2), 1)
        self.assertEqual(self.blockchain.get_votes_for_candidate(3), 0)
    
    def test_verify_vote(self):
        """Test checking if a voter has voted"""
        # Initially no votes
        self.assertFalse(self.blockchain.verify_vote(1))
        
        # Add a vote
        self.blockchain.add_block({'voter_id': 1, 'candidate_id': 1})
        
        # Now voter 1 has voted
        self.assertTrue(self.blockchain.verify_vote(1))
        self.assertFalse(self.blockchain.verify_vote(2))
    
    def test_proof_of_work(self):
        """Test that proof of work is applied"""
        vote_data = {'voter_id': 1, 'candidate_id': 1}
        block = self.blockchain.add_block(vote_data)
        
        # Check that hash has required leading zeros
        self.assertTrue(block.hash.startswith('0' * self.blockchain.difficulty))
        
        # Check that nonce was incremented
        self.assertGreater(block.nonce, 0)
    
    def test_get_chain(self):
        """Test getting the entire blockchain"""
        self.blockchain.add_block({'voter_id': 1, 'candidate_id': 1})
        chain = self.blockchain.get_chain()
        
        self.assertEqual(len(chain), 2)
        self.assertIsInstance(chain[0], dict)
        self.assertIn('hash', chain[0])
