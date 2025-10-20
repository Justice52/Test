#!/bin/bash
# Demo script for E-Voting System with Blockchain

echo "=================================================="
echo "E-Voting System with Blockchain - Demo Script"
echo "=================================================="
echo ""

# Check if Django is installed
if ! python3 -m django --version &> /dev/null; then
    echo "Error: Django is not installed. Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if migrations have been applied
if [ ! -f "db.sqlite3" ]; then
    echo "Setting up database..."
    python3 manage.py migrate
    echo ""
fi

# Check if superuser exists
echo "Creating admin user (if not exists)..."
python3 manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created: username=admin, password=admin123')
else:
    print('Admin user already exists')
" 2>/dev/null
echo ""

# Populate sample data
if [ -f "populate_data.py" ]; then
    echo "Checking for sample data..."
    python3 populate_data.py 2>/dev/null || true
    echo ""
fi

echo "=================================================="
echo "Starting Development Server..."
echo "=================================================="
echo ""
echo "The application will be available at:"
echo "  🌐 Main site: http://127.0.0.1:8000/"
echo "  🔐 Admin panel: http://127.0.0.1:8000/admin/"
echo ""
echo "Sample Credentials:"
echo "  Admin: username=admin, password=admin123"
echo "  Voters: username=voter1-5, password=voter123"
echo ""
echo "Features to explore:"
echo "  ✓ View active elections"
echo "  ✓ Browse candidates"
echo "  ✓ Cast votes (requires login)"
echo "  ✓ View real-time results"
echo "  ✓ Explore blockchain"
echo "  ✓ Verify blockchain integrity"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Start the server
python3 manage.py runserver
