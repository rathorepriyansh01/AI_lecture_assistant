from backend.providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):

    def invoke(

        self,

        prompt

    ):

        return "Dummy Response"

    def health_check(self):

        return {

            "status": "healthy"

        }


provider = DummyProvider(

    api_key="123",

    model="dummy-model"

)

print(provider)

print()

print(provider.provider_info())

print()

print(provider.health_check())

print()

print(provider.invoke("Hello"))