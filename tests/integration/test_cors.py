import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask.testing import FlaskClient

from tests.fixtures.client import client


def test_cors_preflight(client: FlaskClient) -> None:
    endpoints = ['/questify', '/v2/questify']
    origins = [
        "http://localhost:*",
        "https://questify-to-do.vercel.app",
        "http://questify-to-do.s3-website-us-east-1.amazonaws.com"
    ]

    for endpoint in endpoints:
        for origin in origins:
            response = client.options(
                endpoint,
                headers={
                    'Origin': origin,
                    'Access-Control-Request-Method': 'POST'
                }
            )

            assert response.status_code == 200
            assert 'Access-Control-Allow-Origin' in response.headers
            assert origin in response.headers.get('Access-Control-Allow-Origin')
            assert 'Access-Control-Allow-Methods' in response.headers
            assert 'POST' in response.headers.get('Access-Control-Allow-Methods')
