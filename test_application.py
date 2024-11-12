from application import application

def test_hello_elastic_beanstalk():
    # Sets up a test client for the Flask app
    client = application.test_client()
    response = client.get('/')  # Sends a GET request to the root endpoint
    assert response.data == b'Hello Elastic Beanstalk!'  # Checks the response data
    assert response.status_code == 200  # Verifies the response status code is 200 (OK)
