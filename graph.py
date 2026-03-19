from langgraph.graph import StateGraph, END
from config.shared_state import Shared_State as State
from agents import (
    orchestrator_entry,
    orchestrator_relay,
    orchestrator_final,
    story_agent,
    image_agent,
)


def _ok_or_error(state: State) -> str:
    return "error" if state.get("error") else "ok"


def build() -> StateGraph:
    g = StateGraph(State)

    g.add_node("orch_entry",  orchestrator_entry)
    g.add_node("story",       story_agent)
    g.add_node("orch_relay",  orchestrator_relay)
    g.add_node("image",       image_agent)
    g.add_node("orch_final",  orchestrator_final)

    g.set_entry_point("orch_entry")
    g.add_edge("orch_entry", "story")

    g.add_conditional_edges("story",
        _ok_or_error, {"ok": "orch_relay", "error": END})

    g.add_edge("orch_relay", "image")

    g.add_conditional_edges("image",
        _ok_or_error, {"ok": "orch_final", "error": END})

    g.add_edge("orch_final", END)

    return g.compile()