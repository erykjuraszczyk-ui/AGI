"""Privacy-aware provider selection; intentionally no network implementation."""
from cortana.contracts.providers import ModelProvider, ModelRequest, ModelResponse, ProviderKind


class ModelRouter:
    def __init__(self, local: ModelProvider, cloud: ModelProvider | None = None) -> None:
        if local.kind is not ProviderKind.LOCAL:
            raise ValueError("The local provider must declare ProviderKind.LOCAL")
        if cloud is not None and cloud.kind is not ProviderKind.CLOUD:
            raise ValueError("The cloud provider must declare ProviderKind.CLOUD")
        self._local = local
        self._cloud = cloud

    async def generate(self, request: ModelRequest, prefer_cloud: bool = False) -> ModelResponse:
        # Sensitive requests are always kept local by the baseline policy.
        if request.contains_sensitive_data:
            return await self._local.generate(request)
        if prefer_cloud and request.cloud_authorized and self._cloud is not None:
            return await self._cloud.generate(request)
        return await self._local.generate(request)
