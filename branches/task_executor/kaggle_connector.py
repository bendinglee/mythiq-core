def trigger_kaggle_notebook(notebook_id, token, params):
    import requests
    headers = { "Authorization": f"Bearer {token}" }
    response = requests.post(
        f"https://www.kaggle.com/api/v1/notebooks/{notebook_id}/run",
        headers=headers,
        json=params
    )
    return response.json()
