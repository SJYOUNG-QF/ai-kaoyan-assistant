"use client";

export default function AiThinking() {
  return (
    <div className="flex items-center gap-1.5 py-2">
      <div className="flex gap-1">
        <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-400 [animation-delay:0ms]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-400 [animation-delay:150ms]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-400 [animation-delay:300ms]" />
      </div>
      <span className="text-xs text-zinc-400">AI 正在思考</span>
    </div>
  );
}
