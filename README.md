# E-Voting System with Blockchain Backend

A secure and transparent electronic voting system built with Django and blockchain technology. This system ensures vote integrity through cryptographic hashing and an immutable blockchain structure.

## Features

- 🔒 **Secure Voting**: Votes are stored on an immutable blockchain using SHA-256 hashing
- 🔍 **Transparent**: All votes are verifiable on the blockchain while maintaining voter anonymity
- ⚡ **Real-time Results**: Instant vote counting and result visualization
- 🗳️ **Multiple Elections**: Support for multiple concurrent elections
- 👥 **User Management**: Separate admin and voter interfaces
- 📊 **Result Analytics**: Visual representation of election results with percentages
- 🔐 **Proof of Work**: Simple proof-of-work algorithm to secure the blockchain

## Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Blockchain**: Custom implementation using Python's hashlib
- **Frontend**: HTML, CSS (embedded in templates)

## Blockchain Implementation

The system implements a custom blockchain with the following features:

- **Block Structure**: Each block contains index, timestamp, vote data, previous hash, nonce, and current hash
- **Proof of Work**: Mining algorithm requiring leading zeros in block hash
- **Chain Validation**: Built-in validation to ensure blockchain integrity
- **Immutability**: Once a vote is recorded, it cannot be altered

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Justice52/Test.git
   cd Test
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (if not already created)
   ```bash
   python manage.py createsuperuser
   ```

5. **Populate sample data** (optional)
   ```bash
   python populate_data.py
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Administrators

1. Login to the admin panel at `/admin/`
2. Create elections with start and end dates
3. Add candidates for each election
4. Register voters and assign voter IDs
5. Monitor voting progress and view results

### For Voters

1. Login with your voter credentials
2. Browse active elections
3. Select an election and view candidates
4. Cast your vote (one vote per election)
5. Receive blockchain confirmation
6. View real-time results

### Sample Credentials

After running `populate_data.py`:

- **Admin**: username: `admin`, password: `admin123`
- **Voters**: username: `voter1-5`, password: `voter123`

## Project Structure

```
Test/
├── evoting_system/         # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── voting/                 # Main voting application
│   ├── models.py          # Database models (Election, Candidate, Voter, Vote)
│   ├── views.py           # View functions for handling requests
│   ├── admin.py           # Admin interface configuration
│   ├── blockchain.py      # Blockchain implementation
│   ├── urls.py            # URL routing
│   └── templates/         # HTML templates
├── manage.py              # Django management script
├── populate_data.py       # Script to create sample data
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Models

### Election
- Represents an election event with title, description, start/end dates
- Can be active or inactive

### Candidate
- Represents a candidate in an election
- Linked to a specific election
- Vote counts retrieved from blockchain

### Voter
- Extends Django User model
- Has unique voter ID
- Tracks voting status

### Vote
- Records vote in database for quick reference
- Links to voter, candidate, and election
- Stores blockchain hash for verification
- Ensures one vote per voter per election

## Blockchain API

The blockchain can be accessed programmatically:

```python
from voting.blockchain import blockchain

# Add a vote to blockchain
block = blockchain.add_block({
    'voter_id': 1,
    'candidate_id': 2,
    'election_id': 1,
    'timestamp': str(timezone.now())
})

# Get vote count for a candidate
votes = blockchain.get_votes_for_candidate(candidate_id)

# Verify if a voter has voted
has_voted = blockchain.verify_vote(voter_id)

# Check blockchain validity
is_valid = blockchain.is_chain_valid()

# Get entire blockchain
chain = blockchain.get_chain()
```

## Security Features

1. **Cryptographic Hashing**: SHA-256 hashing for all blocks
2. **Proof of Work**: Mining algorithm prevents easy manipulation
3. **Chain Validation**: Automatic validation of blockchain integrity
4. **One Vote Per Election**: Database constraints prevent duplicate voting
5. **CSRF Protection**: Django's built-in CSRF protection for all forms
6. **Password Security**: Django's secure password hashing

## Future Enhancements

- [ ] Multi-factor authentication for voters
- [ ] Email notifications for election updates
- [ ] Export results to PDF/CSV
- [ ] Advanced analytics dashboard
- [ ] Distributed blockchain across multiple nodes
- [ ] Mobile application
- [ ] Voter identity verification using biometrics
- [ ] Real-time blockchain synchronization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a demonstration project for educational purposes. For production use, additional security measures and auditing should be implemented.