import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]
for layer in ("4_skills", "2_orchestrator", "1_interface"):
    sys.path.insert(0, str(AGENT_ROOT / layer))
