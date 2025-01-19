from urllib.parse import urlparse

class PublicUrl:
    def __init__(self, url: str):
        parsed_url = urlparse(url)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError(f"Invalid URL: {url}")
        self._url = url

    @property
    def value(self) -> str:
        """Returns the underlying URL as a string."""
        return self._url

    def __str__(self) -> str:
        return self._url

    def __eq__(self, other) -> bool:
        """Checks equality with another PublicUrl."""
        if isinstance(other, PublicUrl):
            return self._url == other._url
        return False

    def __repr__(self) -> str:
        return f"PublicUrl(url={self._url!r})"
