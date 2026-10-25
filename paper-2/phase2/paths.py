"""Portable repository paths. LLMJ_ROOT (env) overrides the default, which is two levels above this file (…/LLM-J)."""
import os
PHASE2 = os.path.dirname(os.path.abspath(__file__))
LLMJ = os.environ.get("LLMJ_ROOT", os.path.abspath(os.path.join(PHASE2, "..", "..")))
PILOT = os.path.join(LLMJ, "paper-2", "idea-stage", "pilot")
