"""Tests for date filter functionality in graftql."""
def test_date_year(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                students { many(filter: {birthDate: {year: 1999}}) {
                    edges { node { id name birthDate } }
                } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["students"]["many"]["edges"]
    assert len(data) == 2
    names = {e["node"]["name"] for e in data}
    assert names == {"Some Name", "Other Name"}


def test_date_range(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                students { many(filter: {birthDate: {range: ["1998-04-01", "1999-08-25"]}}) {
                    edges { node { id name birthDate } }
                } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["students"]["many"]["edges"]
    assert len(data) == 2
    names = {e["node"]["name"] for e in data}
    assert names == {"Other Name", "Another Name"}


def test_date_items(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                students { many(filter: {birthDate: {items: "1999-09-16"}}) {
                    edges { node { id name birthDate } }
                } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["students"]["many"]["edges"]
    assert len(data) == 1
    assert data[0]["node"]["name"] == "Some Name"


def test_date_nested_year(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                courses { many { edges { node {
                    id name teacherId
                    students {
                        student(filters: {birthDate: {year: 1998}}) { name }
                    }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["courses"]["many"]["edges"]
    assert len(data) == 2


def test_date_nested_range(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                courses { many { edges { node {
                    students {
                        student(filters: {birthDate: {range: ["1999-08-01", "1999-10-25"]}}) { name }
                    }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["courses"]["many"]["edges"]
    assert len(data) == 2


def test_date_nested_items(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                courses { many { edges { node {
                    students {
                        student(filters: {birthDate: {items: ["1999-07-24"]}}) { name }
                    }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["courses"]["many"]["edges"]
    assert len(data) == 2
