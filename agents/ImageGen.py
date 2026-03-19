import os
import torch
from diffusers import StableDiffusionPipeline
from langchain_core.messages import AIMessage
from config.shared_state import Shared_State as State
from utils.logger import log

log.agent("image", "Loading model ")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,   
    safety_checker=None,         
)

pipe.enable_attention_slicing()  

if torch.cuda.is_available():
    pipe = pipe.to("cuda")
    log.agent("image", "GPU ")
else:
    pipe = pipe.to("cpu")
    log.agent("image", "CPU ")

log.agent("image", "Model ready")


def image_agent(state: State) -> dict:
    log.agent("image", "Building image prompt...")
    try:
        story = state["story"]
        sentences = [s.strip() for s in story.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        base = ". ".join(sentences[:2])
        image_prompt = f"{base}. digital painting, highly detailed, vivid colors."

        log.agent("image", f'Prompt: "{image_prompt[:70]}..."')
        log.agent("image", "Generating image locally...")

        result = pipe(
            prompt=image_prompt,
            num_inference_steps=20,   # lower = faster, less quality (20 is good balance)
            guidance_scale=7.5,
            height=512,               # 512x512 uses much less RAM than 1024
            width=512,
        )
        image = result.images[0]

        out_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "output.png")
        )
        image.save(out_path)
        log.agent("image", f"Done! Image saved → {out_path}")

        return {
            "messages": [AIMessage(content=out_path, name="image_agent")],
        }

    except Exception as e:
        log.error(f"Image Agent: {e}")
        return {"error": str(e)}