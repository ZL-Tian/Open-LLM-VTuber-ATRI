import asyncio
import hashlib
import threading
from contextlib import asynccontextmanager
from typing import AsyncIterator

from loguru import logger


BackendKey = tuple[str, str, str, str, str]
RegistryKey = tuple[int, BackendKey]

_registry_lock = threading.Lock()
_limiters: dict[RegistryKey, asyncio.Semaphore] = {}
_limits: dict[RegistryKey, int] = {}


def build_backend_key(
    provider_name: str,
    base_url: str | None,
    organization_id: str | None = None,
    project_id: str | None = None,
    api_key: str | None = None,
) -> BackendKey:
    api_key_fingerprint = ""
    if api_key:
        api_key_fingerprint = hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]

    return (
        provider_name,
        base_url or "",
        organization_id or "",
        project_id or "",
        api_key_fingerprint,
    )


def _normalize_limit(max_concurrent_requests: int | None) -> int:
    if max_concurrent_requests is None:
        return 1
    return max(1, int(max_concurrent_requests))


def _get_request_limiter(
    backend_key: BackendKey, max_concurrent_requests: int | None
) -> asyncio.Semaphore:
    normalized_limit = _normalize_limit(max_concurrent_requests)
    loop_id = id(asyncio.get_running_loop())
    registry_key = (loop_id, backend_key)

    with _registry_lock:
        limiter = _limiters.get(registry_key)
        current_limit = _limits.get(registry_key)

        if limiter is None or current_limit != normalized_limit:
            limiter = asyncio.Semaphore(normalized_limit)
            _limiters[registry_key] = limiter
            _limits[registry_key] = normalized_limit

        return limiter


@asynccontextmanager
async def limit_request_concurrency(
    backend_key: BackendKey,
    max_concurrent_requests: int | None,
) -> AsyncIterator[None]:
    limiter = _get_request_limiter(backend_key, max_concurrent_requests)

    if limiter.locked():
        logger.debug(
            f"Waiting for an available LLM request slot for backend '{backend_key[1] or backend_key[0]}'."
        )

    await limiter.acquire()
    try:
        yield
    finally:
        limiter.release()
