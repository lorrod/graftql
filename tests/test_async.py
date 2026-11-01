"""Tests for asynchronous database engine support in graftql."""
async def test_async_put(client_async):
    response = await client_async.post(
        "/graphql",
        json={
            "query": """mutation {
                users { put(input: {name: "Some Name", qtd: 10}) { id name qtd } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"users": {"put": {"id": 1, "name": "Some Name", "qtd": 10}}}}


async def test_async_query(client_async):
    response = await client_async.post(
        "/graphql",
        json={
            "query": """query {
                users { many { edges { node { id name qtd } } } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {"users": {"many": {"edges": [{"node": {"id": 1, "name": "Some Name", "qtd": 10}}]}}}
    }


async def test_async_put_with_key(client_async):
    response = await client_async.post(
        "/graphql",
        json={
            "query": """mutation {
                users { put(input: {id: 2, name: "Other Name", qtd: 8}) { id } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"users": {"put": {"id": 2}}}}


async def test_async_update(client_async):
    response = await client_async.post(
        "/graphql",
        json={
            "query": """mutation {
                users { put(input: {id: 1, name: "Another Name", qtd: 7}) { id name qtd } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {"users": {"put": {"id": 1, "name": "Another Name", "qtd": 7}}}
    }


async def test_async_delete(client_async):
    response = await client_async.post(
        "/graphql",
        json={
            "query": """mutation {
                users { delete(input: {id: 1}) { id } }
            }"""
        },
    )
    assert response.status_code == 200
    assert response.json() == {"data": {"users": {"delete": {"id": 1}}}}
