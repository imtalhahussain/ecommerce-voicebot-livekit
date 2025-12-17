from livekit.agents import WorkerOptions, run_app
from agent.livekit_agent import entrypoint

if __name__ == "__main__":
    run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
