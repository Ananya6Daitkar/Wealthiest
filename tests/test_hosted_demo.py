import pytest
from fastapi.testclient import TestClient
from nestproof.app import create_app


def test_hosted_gate_protects_pages_and_api(tmp_path, monkeypatch):
    monkeypatch.setenv('NESTPROOF_DEMO_PASSWORD', 'test-only-demo-password')
    with TestClient(create_app(tmp_path / 'demo.db'), base_url='https://example.test') as client:
        assert client.get('/healthz').text == 'ok'
        for path in ('/', '/static/index.html', '/api/docs', '/api/documents'):
            assert client.get(path).status_code == 401
        for header in ('Basic !!', 'Bearer invalid', 'Basic /w=='):
            assert client.get('/', headers={'Authorization': header}).status_code == 401
        assert client.get('/', auth=('judge', 'wrong')).status_code == 401
        assert client.get('/', auth=('judge', 'test-only-demo-password')).status_code == 200
        response = client.post('/api/session', json={'persona': 'ananya'}, auth=('judge', 'test-only-demo-password'))
        assert response.status_code == 200
        assert 'Secure' in response.headers['set-cookie']


def test_render_fails_closed_without_password(tmp_path, monkeypatch):
    monkeypatch.setenv('RENDER', 'true')
    monkeypatch.delenv('NESTPROOF_DEMO_PASSWORD', raising=False)
    with pytest.raises(RuntimeError, match='requires'):
        create_app(tmp_path / 'demo.db')
