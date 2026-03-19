import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from config.shared_state import Shared_State as  State
from config.prompt  import STORY_SYSTEM
from utils.logger import log

def story_agent(state: State) -> dict:
    log.agent("story", "Generating story...")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.9,
            google_api_key=os.getenv("API_STORY"),
        )
        response = llm.invoke([
            SystemMessage(content=STORY_SYSTEM),
            HumanMessage(content=state["user_input"]),
        ])
        story = response.content.strip()
        log.agent("story", f"Done — {len(story.split())} words.")
        return {
            "story": story,
            "messages": [AIMessage(content=story, name="story_agent")],
        }
    except Exception as e:
        log.error(f"Story Agent: {e}")
        return {"error": str(e)}