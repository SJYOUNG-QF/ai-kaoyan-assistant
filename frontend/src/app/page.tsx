"use client";

import { useState } from "react";
import PdfUploadPanel from "./components/PdfUploadPanel";
import ChatPanel from "./components/ChatPanel";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [textLength, setTextLength] = useState(0);
  const [textPreview, setTextPreview] = useState("");
  const [testMode, setTestMode] = useState(false);

  const handleUploaded = (file: File, length: number, preview: string) => {
    setSelectedFile(file);
    setTextLength(length);
    setTextPreview(preview);
  };

  return (
    <div className="flex flex-1 flex-col h-full max-h-screen">
      {/* 顶部标题栏 */}
      <header className="shrink-0 border-b border-zinc-200/60 bg-white/80 backdrop-blur px-6 py-3 dark:border-zinc-800 dark:bg-zinc-950/80">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
              <span className="text-sm font-bold text-white">AI</span>
            </div>
            <h1 className="text-lg font-bold text-zinc-800 dark:text-zinc-100">
              AI 考研学习助手
            </h1>
          </div>
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <span className="text-xs font-medium text-zinc-400">测试模式</span>
            <button
              onClick={() => setTestMode(!testMode)}
              className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                testMode ? "bg-amber-500" : "bg-zinc-300 dark:bg-zinc-600"
              }`}
            >
              <span
                className={`inline-block h-3.5 w-3.5 rounded-full bg-white shadow-sm transition-transform ${
                  testMode ? "translate-x-4.5" : "translate-x-0.5"
                }`}
              />
            </button>
          </label>
        </div>
      </header>

      {/* 测试模式横幅 */}
      {testMode && (
        <div className="shrink-0 flex items-center justify-center gap-2 bg-amber-50 px-6 py-2 text-center text-xs font-medium text-amber-700 dark:bg-amber-950/50 dark:text-amber-400">
          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          当前为测试文本模式 — 使用内置考研数学资料，无需上传 PDF
        </div>
      )}

      {/* 主内容区 */}
      <main className="flex flex-1 overflow-hidden">
        <PdfUploadPanel
          selectedFile={selectedFile}
          textLength={textLength}
          onUploaded={handleUploaded}
        />
        <ChatPanel
          selectedFile={selectedFile}
          textPreview={textPreview}
          testMode={testMode}
        />
      </main>
    </div>
  );
}
