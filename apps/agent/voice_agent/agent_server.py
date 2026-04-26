from __future__ import annotations

import json
import logging

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    TurnHandlingOptions,
    WorkerPermissions,
    inference,
    room_io,
)
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from voice_agent.config import Settings
from voice_agent.models import VoiceCapabilities, VoiceSessionInfo

load_dotenv()
settings = Settings.from_env()
logger = logging.getLogger("auralis-agent")

SYSTEM_INSTRUCTIONS = (
    "You are Auralis, a helpful realtime AI voice agent. "
    "Speak briefly, clearly, and naturally. "
    "You are a conversational voice assistant for this demo, not a tool-using "
    "personal assistant. "
    "You can answer general questions, explain concepts, brainstorm ideas, "
    "help with writing, summarize or reason over text the user provides, "
    "offer planning help, and discuss coding or product ideas. "
    "You do not have live web browsing, weather, calendar, reminders, music "
    "playback, booking, email, file access, or external app control. "
    "When asked what you can do, describe only those available conversational "
    "abilities and do not claim unavailable tools. "
    "If the user asks for unavailable tool actions, say you cannot perform "
    "that action directly, then offer a useful conversational alternative. "
    "Keep responses conversational, allow interruptions, and ask follow-up "
    "questions only when they improve the conversation. "
    "If you are unsure about a fact, say so plainly instead of guessing."
)

OPENING_MESSAGE = (
    "Hello, I am Auralis. I am ready whenever you want to start talking."
)

server = AgentServer(
    permissions=WorkerPermissions(
        can_publish=True,
        can_subscribe=True,
        can_publish_data=True,
        can_update_metadata=True,
        hidden=False,
    )
)


def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


class AuralisVoiceAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTIONS)


async def _publish_metadata(ctx: JobContext) -> None:
    capabilities = VoiceCapabilities(
        stt_model=settings.stt_model,
        llm_model=settings.llm_model,
        tts_model=settings.tts_model,
        tts_voice=settings.tts_voice,
    )
    session_info = VoiceSessionInfo(
        session_id=ctx.room.name,
        agent_name=settings.livekit_agent_name,
    )
    await ctx.room.local_participant.set_attributes(
        {
            "app.voice.capabilities": json.dumps(capabilities.to_payload()),
            "app.voice.session": json.dumps(session_info.to_payload()),
        }
    )


@server.rtc_session(agent_name=settings.livekit_agent_name)
async def entrypoint(ctx: JobContext) -> None:
    turn_detector = MultilingualModel()

    session = AgentSession(
        stt=inference.STT(model=settings.stt_model),
        llm=inference.LLM(model=settings.llm_model),
        tts=inference.TTS(model=settings.tts_model, voice=settings.tts_voice),
        vad=ctx.proc.userdata["vad"],
        turn_handling=TurnHandlingOptions(
            turn_detection=turn_detector,
            preemptive_generation={"enabled": True},
        ),
    )

    @session.on("agent_state_changed")
    def on_agent_state_changed(event) -> None:
        logger.info(
            "agent state changed",
            extra={
                "old_state": event.old_state,
                "new_state": event.new_state,
            },
        )

    @session.on("user_input_transcribed")
    def on_user_input_transcribed(event) -> None:
        if not event.is_final:
            return
        logger.info(
            "user input transcribed",
            extra={"transcript": event.transcript.strip()},
        )

    await session.start(
        room=ctx.room,
        agent=AuralisVoiceAgent(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
            text_input=True,
        ),
    )
    await ctx.connect()
    await _publish_metadata(ctx)
    session.say(OPENING_MESSAGE)
