import clsx from "clsx";

type VoiceOrbProps = {
  state:
    | "idle"
    | "connecting"
    | "listening"
    | "thinking"
    | "speaking"
    | "reconnecting"
    | "failed";
  isInterrupted?: boolean;
};

export function VoiceOrb({ state, isInterrupted = false }: VoiceOrbProps) {
  const liveState =
    state === "listening" || state === "thinking" || state === "speaking";
  const showWaveform =
    state === "listening" || state === "thinking" || state === "speaking";

  return (
    <div className="voice-orb-shell relative flex h-[18rem] items-center justify-center sm:h-[21rem]">
      <div
        className={clsx(
          "voice-orb-ring absolute h-44 w-44 rounded-full sm:h-56 sm:w-56",
          liveState && "voice-orb-ring-active",
          (state === "failed" || state === "reconnecting") &&
            "voice-orb-ring-failed",
          state === "thinking" && "voice-orb-ring-thinking",
          state === "speaking" && "voice-orb-ring-speaking",
          isInterrupted && "voice-orb-ring-interrupted",
        )}
      />
      <div
        className={clsx(
          "voice-orb-ring absolute h-32 w-32 rounded-full delay-150 sm:h-44 sm:w-44",
          liveState && "voice-orb-ring-active",
          (state === "failed" || state === "reconnecting") &&
            "voice-orb-ring-failed",
          state === "thinking" && "voice-orb-ring-thinking",
          state === "speaking" && "voice-orb-ring-speaking",
          isInterrupted && "voice-orb-ring-interrupted",
        )}
      />
      <div
        className={clsx(
          "voice-orb-core flex h-28 w-28 items-center justify-center rounded-full text-sm font-semibold uppercase tracking-[0.32em] sm:h-36 sm:w-36",
          state === "idle" && "voice-orb-core-idle",
          state === "connecting" && "voice-orb-core-connecting",
          state === "listening" && "voice-orb-core-listening",
          state === "thinking" && "voice-orb-core-thinking",
          state === "speaking" && "voice-orb-core-speaking",
          state === "reconnecting" && "voice-orb-core-reconnecting",
          state === "failed" && "voice-orb-core-failed",
          isInterrupted && "voice-orb-core-interrupted",
        )}
      >
        <div className="flex flex-col items-center gap-2">
          {showWaveform && (
            <div
              className={clsx(
                "voice-orb-waveform",
                state === "listening" && "voice-orb-waveform-listening",
                state === "thinking" && "voice-orb-waveform-thinking",
                state === "speaking" && "voice-orb-waveform-speaking",
              )}
              aria-hidden="true"
            >
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>
          )}
          <span className="text-[0.58rem] text-white/70">Auralis</span>
          <span className="text-[0.7rem] text-white">Voice</span>
        </div>
      </div>
    </div>
  );
}
