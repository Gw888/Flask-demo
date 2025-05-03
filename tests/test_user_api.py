import json
import io
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_user(client):
    response = client.post('/api/users', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['data']['username'] == 'testuser'

def test_get_users(client):
    client.post('/api/users', json={
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'password123'
    })
    response = client.get('/api/users')
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)

def test_upload_file(client):
    data = {
        'file': (io.BytesIO(b'my file contents'), 'test.txt')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert 'filename' in response.json
