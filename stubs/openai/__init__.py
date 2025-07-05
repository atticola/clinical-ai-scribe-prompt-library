class OpenAIError(Exception): ...
class _Fake:
    def __getattr__(self, _): return self
    def __call__(self, *_, **__): return "STUB"
Completion = ChatCompletion = _Fake()
