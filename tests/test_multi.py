"""Tests for multi-engine/multi-database support in graftql."""
def test_multi_query(client_data):
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
    data = response.json()["data"]["teachers"]["many"]["edges"]
    assert len(data) == 1
    teacher = data[0]["node"]
    assert teacher["name"] == "Some Teacher"
    assert len(teacher["courses"]) == 2


def test_multi_query_one(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                courses { many { edges { node {
                    name
                    teacher { name }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = [e["node"] for e in response.json()["data"]["courses"]["many"]["edges"]]
    assert len(nodes) == 2
    for node in nodes:
        assert node["teacher"]["name"] == "Some Teacher"


def test_multi_key(client_data):
    response = client_data.post(
        "/graphql",
        json={
            "query": """query {
                students { many { edges { node {
                    name birthDate
                    courses {
                        course { name }
                        grader { semester grade }
                    }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]["students"]["many"]["edges"]
    assert len(data) == 3
    # Verify relationships loaded correctly
    some_name = next(e["node"] for e in data if e["node"]["name"] == "Some Name")
    assert len(some_name["courses"]) == 2
    assert any(c["course"]["name"] == "Mathematics" for c in some_name["courses"])
