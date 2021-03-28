import run


def test_home():
    """
    Test that home page loads fine
    :return:
    """
    c = run.app.test_client()
    response = c.get('/')
    response_data = response.data

    assert 'Hi there' in response_data
