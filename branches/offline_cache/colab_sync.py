def sync_with_colab(repo_url):
    import requests
    try:
        res = requests.get(repo_url)
        if res.status_code == 200:
            return { "status": "synced", "content": res.text[:500] }
        else:
            return { "error": f"{res.status_code}" }
    except Exception as e:
        return { "error": str(e) }
