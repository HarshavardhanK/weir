import os
import pytest
import psycopg2
from app.agents.utils.postgres_utils import store_memory_in_db, retrieve_memory_from_db

# Mock environment variable for testing
os.environ['DATABASE_URL'] = 'postgresql://weir:password@localhost:5432/weirdb'

@pytest.fixture(scope='module')
def db_connection():
    # Setup: Create a connection to the test database
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    # Create the memories table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        user_id VARCHAR PRIMARY KEY,
        memory_data JSONB
    );
    """)
    conn.commit()
    yield conn
    # Teardown: Close the connection
    conn.close()

def test_store_memory_in_db(db_connection):
    user_id = 'test_user'
    memory_data = {'messages': ['Test message']}
    
    # Test storing memory
    result = store_memory_in_db(user_id, memory_data)
    assert result['status'] == 'success'
    assert result['message'] == 'Memory stored successfully'

def test_retrieve_memory_from_db(db_connection):
    user_id = 'test_user'
    
    # Test retrieving memory
    result = retrieve_memory_from_db(user_id)
    assert result['status'] == 'success'
    assert 'memory_data' in result
    assert result['memory_data'] == {'messages': ['Test message']}

def test_retrieve_memory_from_db_no_data(db_connection):
    user_id = 'non_existent_user'
    
    # Test retrieving memory for a non-existent user
    result = retrieve_memory_from_db(user_id)
    assert result['status'] == 'error'
    assert result['message'] == 'No memory found for user'