def fetch_data(config):
    provider = config.get("provider", "weather")
    from .provider_map import PROVIDERS
    return { "provider": provider, "url": PROVIDERS.get(provider, "unknown") }
