"use client";

import { useState, useRef, useEffect } from "react";
import { askQuestion, type ChatMessage } from "@/lib/api";
import MarkdownRenderer from "./MarkdownRenderer";
import AiThinking from "./AiThinking";

type ChatStatus = "idle" | "loading" | "done";

interface Props {
  selectedFile: File | null;
  textPreview: string;
  testMode: boolean;
}

export default function ChatPanel({ selectedFile, textPreview, testMode }: Props) {
  const canChat = testMode || !!selectedFile;
  const [question, setQuestion] = useState("");
  const [chatStatus, setChatStatus] = useState<ChatStatus>("idle");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, chatStatus]);

  const handleAsk = async () => {
    const trimmed = question.trim();
    if (!trimmed || !canChat || chatStatus === "loading") return;

    const userMsg: ChatMessage = { role: "user", content: trimmed };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setQuestion("");
    setChatStatus("loading");

    try {
      const data = await askQuestion(
        trimmed,
        selectedFile?.name || "",
        messages,
        testMode,
      );
      const aiMsg: ChatMessage = { role: "assistant", content: data.answer };
      setMessages([...updatedMessages, aiMsg]);
      setChatStatus("done");
    } catch (err: any) {
      const errMsg: ChatMessage = {
        role: "assistant",
        content: `> 错误: ${err.message || "请求失败"}`,
      };
      setMessages([...updatedMessages, errMsg]);
      setChatStatus("done");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const prevFileName = useRef(selectedFile?.name);
  if (selectedFile?.name !== prevFileName.current) {
    prevFileName.current = selectedFile?.name;
    if (messages.length > 0) {
      setMessages([]);
    }
  }

  return (
    <section className="flex flex-1 flex-col bg-white dark:bg-zinc-950">
      {/* 消息区 */}
      <div className="flex flex-1 flex-col overflow-auto p-6">
        {/* 空状态：未上传文件且无消息 */}
        {messages.length === 0 && !textPreview && chatStatus !== "loading" && (
          <div className="flex flex-1 items-center justify-center">
            <div className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
                <span className="text-2xl font-bold text-white">AI</span>
              </div>
              <p className="mb-1 text-sm font-medium text-zinc-500 dark:text-zinc-400">
                {testMode ? "测试模式已开启" : "AI 考研学习助手"}
              </p>
              <p className="text-xs text-zinc-400 dark:text-zinc-500">
                {testMode
                  ? "直接输入问题，AI 将基于内置考研资料回答"
                  : "上传考研资料 PDF 后即可开始提问"}
              </p>
            </div>
          </div>
        )}

        {/* 空状态：已上传文件但还没提问，显示 PDF 预览 */}
        {messages.length === 0 && textPreview && chatStatus !== "loading" && (
          <div className="flex flex-1 items-center justify-center">
            <div className="max-w-lg text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-green-100 dark:bg-green-900">
                <svg className="h-6 w-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="mb-2 text-xs font-semibold text-zinc-400 uppercase tracking-wide">
                PDF 文本提取结果预览
              </p>
              <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-4 text-left text-sm leading-relaxed text-zinc-700 max-h-48 overflow-auto dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300">
                {textPreview}
              </div>
              <p className="mt-3 text-xs text-zinc-400">
                在下方输入问题，AI 将根据资料内容为你解答
              </p>
            </div>
          </div>
        )}

        {/* 对话消息列表 */}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-6 flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
          >
            {/* 头像 */}
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-xs font-bold text-white ${
                msg.role === "user"
                  ? "bg-blue-500"
                  : "bg-gradient-to-br from-purple-500 to-blue-500"
              }`}
            >
              {msg.role === "user" ? "我" : "AI"}
            </div>

            {/* 气泡 */}
            <div
              className={`max-w-[75%] rounded-2xl px-4 py-3 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300"
              }`}
            >
              {msg.role === "assistant" ? (
                <MarkdownRenderer content={msg.content} />
              ) : (
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {msg.content}
                </p>
              )}
            </div>
          </div>
        ))}

        {/* AI 思考动画 */}
        {chatStatus === "loading" && (
          <div className="mb-6 flex gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 text-xs font-bold text-white">
              AI
            </div>
            <div className="rounded-2xl bg-zinc-100 px-4 py-3 dark:bg-zinc-800">
              <AiThinking />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* 输入框 */}
      <div className="shrink-0 border-t border-zinc-200 p-4 dark:border-zinc-800">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              testMode
                ? "输入考研相关问题...（Enter 发送）"
                : "上传 PDF 后在此输入问题...（Enter 发送）"
            }
            disabled={!canChat || chatStatus === "loading"}
            className="flex-1 rounded-xl border border-zinc-300 bg-zinc-50 px-4 py-3 text-sm text-zinc-700 placeholder:text-zinc-400 transition-colors focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100 disabled:opacity-50 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300 dark:focus:border-blue-500 dark:focus:ring-blue-900"
          />
          <button
            onClick={handleAsk}
            disabled={!canChat || !question.trim() || chatStatus === "loading"}
            className="shrink-0 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 px-5 py-3 text-sm font-medium text-white transition-all hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:hover:from-blue-600 disabled:hover:to-blue-700"
          >
            {chatStatus === "loading" ? (
              <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            ) : (
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </section>
  );
}
