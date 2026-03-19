from config.shared_state import Shared_State as State
from utils.logger import log


def orchestrator_entry(state: State) -> dict:
    log.orch(f'Received: "{state.get("user_input")}"')
    log.orch("Routing → Story Agent")
    return {}


def orchestrator_relay(state: State) -> dict:
    log.orch("Story received. Routing → Image Agent")
    return {}


def orchestrator_final(state: State) -> dict:
    log.orch("Pipeline complete ✓")
    return {}