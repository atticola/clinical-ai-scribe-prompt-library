"""
Minimal fake 'langchain' so code imports succeed in offline sandbox.
Only implements the attributes your run_eval.py currently touches.
"""
from types import SimpleNamespace as _S

class _Fake:
    def __init__(self, *_, **__): pass
    def __call__(self, *_, **__): return "STUB"

llms    = _S(OpenAI=_Fake)
prompts = _S(PromptTemplate=_Fake)
chains  = _S(LLMChain=_Fake)
