"""
Unit tests for the Flask application
Place this file in a 'tests' directory in your project root
"""

import pytest
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test instance of the app."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class TestBasicRoutes:
    """Test basic Flask application routes"""
    
    def test_home_page(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_app_is_testing(self, app):
        """Test that the app is in testing mode"""
        assert app.config['TESTING'] is True
    
    def test_404_error(self, client):
        """Test that 404 errors are handled"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404


class TestApplicationHealth:
    """Test application health and configuration"""
    
    def test_app_exists(self, app):
        """Test that app instance exists"""
        assert app is not None
    
    def test_app_is_flask_app(self, app):
        """Test that app is a Flask application"""
        assert hasattr(app, 'route')
        assert hasattr(app, 'test_client')


class TestHTTPMethods:
    """Test HTTP methods"""
    
    def test_get_method(self, client):
        """Test GET method on home route"""
        response = client.get('/')
        assert response.status_code in [200, 404, 405]
    
    def test_post_method_not_allowed(self, client):
        """Test POST method on routes that don't accept it"""
        response = client.post('/nonexistent')
        # Should return 404 or 405
        assert response.status_code in [404, 405]


# Additional test for forms if your app has any
class TestForms:
    """Test form submissions if applicable"""
    
    def test_form_submission(self, client):
        """Test form submission (customize based on your app)"""
        # Example: Test a login or registration form
        # Modify this based on your actual routes
        response = client.post('/submit', data={
            'field1': 'value1',
            'field2': 'value2'
        }, follow_redirects=True)
        # Add appropriate assertions based on your app's behavior
        assert response.status_code in [200, 404, 405]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])