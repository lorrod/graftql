"""Tests for GraphQL permission and auth classes in graftql."""
def test_class_permission(client_auth):
    """Model not in user's allowed classes raises 403."""
    response = client_auth.post(
        "/graphql",
        json={
            "query": """query {
                privates { many { edges { node { id description } } } }
            }"""
        },
    )
    assert response.status_code == 403


def test_query_permission(client_auth):
    """query_filter limits results to allowed categories (A, B)."""
    response = client_auth.post(
        "/graphql",
        json={
            "query": """query {
                resources { many { edges { node { id name category } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = [e["node"] for e in response.json()["data"]["resources"]["many"]["edges"]]
    ids = {n["id"] for n in nodes}
    assert ids == {1, 2}
    categories = {n["category"] for n in nodes}
    assert categories <= {"A", "B"}


def test_dl_filter(client_auth):
    """dl_filter returns only resources with allowed categories."""
    response = client_auth.post(
        "/graphql",
        json={
            "query": """query {
                owners { many { edges { node {
                    id name
                    resources { id category }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = [e["node"] for e in response.json()["data"]["owners"]["many"]["edges"]]
    assert len(nodes) == 1
    resources = nodes[0]["resources"]
    assert len(resources) == 2
    assert all(r["category"] in {"A", "B"} for r in resources)


def test_permission_dl(client_auth):
    """Private relationship returns None when user lacks Private permission."""
    response = client_auth.post(
        "/graphql",
        json={
            "query": """query {
                resources { many { edges { node {
                    id name
                    private { id description }
                } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = [e["node"] for e in response.json()["data"]["resources"]["many"]["edges"]]
    for node in nodes:
        assert node["private"] is None


def test_context_getter(client_auth):
    """context_getter enriches context; owners are accessible."""
    response = client_auth.post(
        "/graphql",
        json={
            "query": """query {
                owners { many { edges { node { id name } } } }
            }"""
        },
    )
    assert response.status_code == 200
    nodes = response.json()["data"]["owners"]["many"]["edges"]
    assert len(nodes) >= 1
