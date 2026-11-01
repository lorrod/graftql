"""Tests for basic CRUD GraphQL operations in graftql."""
def test_insert(client):
    response = client.post(
        "/graphql",
        json={
            "query": """mutation {
                students { put(input: {name: "Some Name", birthDate: "1999-09-16"}) { id } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"students": {"put": {"id": 1}}}}


def test_insert_key(client):
    response = client.post(
        "/graphql",
        json={
            "query": """mutation {
                studentcourses { put(input: {studentId: 1, courseId: 1}) { studentId courseId } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {"studentcourses": {"put": {"studentId": 1, "courseId": 1}}}
    }


def test_read(client):
    response = client.post(
        "/graphql",
        json={
            "query": """query {
                students { many { edges { node { id name birthDate } } } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "students": {
                "many": {"edges": [{"node": {"id": 1, "name": "Some Name", "birthDate": "1999-09-16"}}]}
            }
        }
    }


def test_update(client):
    response = client.post(
        "/graphql",
        json={
            "query": """mutation {
                students { put(input: {id: 1, name: "Some Name Last", birthDate: "1999-09-16"}) { id name } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"students": {"put": {"id": 1, "name": "Some Name Last"}}}}

    response = client.post(
        "/graphql",
        json={
            "query": """query {
                students { many { edges { node { id name birthDate } } } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "students": {
                "many": {
                    "edges": [{"node": {"id": 1, "name": "Some Name Last", "birthDate": "1999-09-16"}}]
                }
            }
        }
    }


def test_delete(client):
    response = client.post(
        "/graphql",
        json={
            "query": """mutation {
                students { delete(input: {id: 1}) { id } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"students": {"delete": {"id": 1}}}}

    response = client.post(
        "/graphql",
        json={"query": """query { students { many { edges { node { id } } } } }"""},
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"students": {"many": {"edges": []}}}}
