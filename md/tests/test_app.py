import sys
import os

sys.path.append("/app")

from manage import app 
import pytest
import json


@pytest.fixture
def client():

    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_client(client):
    with client.session_transaction() as session:
        session['_user_id'] = 1
    return client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index(client):
    response = client.get('/data/')
    assert response.status_code == 200

def test_browse_page(client):
    response = client.get('/data/browse')
    assert response.status_code == 200

def test_create_page(client):
    response = client.get('/data/create')
    assert response.status_code == 200

def test_edit_page(client):
    response = client.get('/data/edit')
    assert response.status_code == 200

def test_instances_page(client):
    response = client.get('/data/instances')
    assert response.status_code == 200

    



def test_create_datastructure(auth_client):
    
    test_datastructure = {
        "name": "Test Structure 8",
        "fields": [
            {"name": "field1", "type": "string"},
            {"name": "field2", "type": "integer"}
        ]
    }
    response = auth_client.post('/data/add_datastructure', 
                          data={'body': json.dumps(test_datastructure)})
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.get_data(as_text=True))
    assert response.status_code == 200
    

def test_create_instance(auth_client):
    test_instance = {
        "name": "Test 8",
        "field1": "test value",
        "field2": 7
    }
    response = auth_client.post('/data/add_instance',
                              data={'body': json.dumps(test_instance)})
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.get_data(as_text=True))
    assert response.status_code == 200

def test_get_change(auth_client):
    # First get all pending changes
    response = auth_client.get('/data/api/pendings')
    pendings = json.loads(response.get_data(as_text=True))
    # Get the first pending datastructure if any exist
    if pendings["Datastructures"]:
        change_id = pendings["Datastructures"][0]
        response = auth_client.get(f'/data/change/{change_id}/datastructure')
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.get_data(as_text=True))
        assert response.status_code == 200

def test_edit_datastructure(auth_client):
    # Get available datastructures
    response = auth_client.get('/data/api/datastructures')
    datastructures = json.loads(response.get_data(as_text=True))
    
    if datastructures:
        structure_id = datastructures[0]  # Get first available ID
        test_datastructure = {
            "name": "Updated Structure 8",
            "fields": [
                {"name": "field1", "type": "string"},
                {"name": "field2", "type": "integer"},
                {"name": "field3", "type": "boolean"}
            ]
        }
        response = auth_client.post('/data/edit_datastructure',
                                  data={
                                      'body': json.dumps(test_datastructure),
                                      'datastructureKey': structure_id
                                  })
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.get_data(as_text=True))
        assert response.status_code == 200

def test_edit_instance(auth_client):
    # Get available instances
    response = auth_client.get('/data/api/instances')
    instances = json.loads(response.get_data(as_text=True))
    

    if instances:
        instance_id = instances[0]  # Get first available ID
        test_instance = {
            "name": "Updated Instance 8",
            "field1": "updated value",
            "field2": 45
        }
        response = auth_client.post('/data/edit_instance',
                                  data={
                                      'body': json.dumps(test_instance),
                                      'instanceKey': instance_id
                                  })
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.get_data(as_text=True))
        assert response.status_code == 200

def test_api_instances(auth_client):
    # Get available instances
    response = auth_client.get('/data/api/instances')

    print("Response Status Code:", response.status_code)
    print("Response Data:", response.get_data(as_text=True))
    assert response.status_code == 200