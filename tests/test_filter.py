"""Tests for GraphQL filter generation and application in graftql."""
def test_query(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                students { many { edges { node { id name birthDate } } } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["students"]["many"]["edges"]
    names = [e["node"]["name"] for e in data]
    assert "Some Name" in names
    assert len(data) == 3


def test_query_filter(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                students { many(filter: {name: "Some Name"}) { edges { node { id name } } } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["students"]["many"]["edges"]
    assert len(data) == 1
    assert data[0]["node"]["name"] == "Some Name"


def test_relationship(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                teachers { many { edges { node {
                    id name
                    courses { id name }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = response.json()["data"]["teachers"]["many"]["edges"]
    assert len(nodes) == 1
    teacher = nodes[0]["node"]
    assert teacher["name"] == "Some Teacher"
    course_names = [c["name"] for c in teacher["courses"]]
    assert "Mathematics" in course_names
    assert "Physics" in course_names


def test_relationship_one(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                courses { many { edges { node {
                    id name teacherId
                    teacher { id name }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = [e["node"] for e in response.json()["data"]["courses"]["many"]["edges"]]
    assert len(nodes) == 2
    for node in nodes:
        assert node["teacher"]["name"] == "Some Teacher"


def test_relationship_filter(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                teachers { many { edges { node {
                    id name
                    courses { id name students { student { id } } }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = response.json()["data"]["teachers"]["many"]["edges"]
    assert len(nodes) == 1


def test_relationship_one_filter(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                courses { many { edges { node {
                    id name
                    teacher(filters: {id: 99}) { id name }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = [e["node"] for e in response.json()["data"]["courses"]["many"]["edges"]]
    for node in nodes:
        assert node["teacher"] is None
