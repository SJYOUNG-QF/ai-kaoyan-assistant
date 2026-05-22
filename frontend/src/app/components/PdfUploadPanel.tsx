"use client";

import { useRef, useState } from "react";
import { uploadPdf } from "@/lib/api";

type UploadStatus = "idle" | "uploading" | "success" | "error";

interface Props {
  selectedFile: File | null;
  textLength: number;
  onUploaded: (file: File, textLength: number, textPreview: string) => void;
}

export default function PdfUploadPanel({
  selectedFile,
  textLength,
  onUploaded,
}: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>("idle");
  const [message, setMessage] = useState("");

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus("uploading");
    setMessage("");

    try {
      const data = await uploadPdf(file);
      setUploadStatus("success");
      setMessage(data.message);
      onUploaded(file, data.text_length, data.text_preview);
    } catch (err: any) {
      setUploadStatus("error");
      setMessage(err.message || "上传失败");
    }
  };

  return (
    <aside className="w-80 shrink-0 border-r border-zinc-200/60 bg-zinc-50/50 p-5 flex flex-col gap-4 dark:border-zinc-800 dark:bg-zinc-900/50">
      {/* 标题 */}
      <div className="flex items-center gap-2">
        <svg className="h-4 w-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">
          学习资料
        </h2>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* 上传区域 */}
      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={uploadStatus === "uploading"}
        className="group flex flex-1 flex-col items-center justify-center rounded-xl border-2 border-dashed border-zinc-300 bg-white p-6 text-center transition-all hover:border-blue-400 hover:bg-blue-50/50 hover:shadow-sm dark:border-zinc-700 dark:bg-zinc-950 dark:hover:border-blue-500 dark:hover:bg-blue-950/50"
      >
        {uploadStatus === "uploading" ? (
          <svg className="mb-3 h-10 w-10 animate-spin text-blue-500" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : (
          <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-100 text-zinc-400 transition-colors group-hover:bg-blue-100 group-hover:text-blue-500 dark:bg-zinc-800 dark:group-hover:bg-blue-900">
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </div>
        )}
        <p className="mb-1 text-sm font-medium text-zinc-600 dark:text-zinc-400">
          {uploadStatus === "uploading" ? "正在上传并解析..." : "上传 PDF 资料"}
        </p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500">
          支持考研资料、教材、笔记等 PDF 文件
        </p>
      </button>

      {/* 上传成功提示 */}
      {uploadStatus === "success" && (
        <div className="flex items-start gap-2 rounded-xl border border-emerald-200 bg-emerald-50 p-3 dark:border-emerald-800 dark:bg-emerald-950">
          <svg className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-xs text-emerald-700 dark:text-emerald-400">{message}</p>
        </div>
      )}

      {/* 上传失败提示 */}
      {uploadStatus === "error" && (
        <div className="flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 p-3 dark:border-red-800 dark:bg-red-950">
          <svg className="mt-0.5 h-4 w-4 shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-xs text-red-700 dark:text-red-400">{message}</p>
        </div>
      )}

      {/* 文件信息卡片 */}
      <div className="rounded-xl border border-zinc-200/60 bg-white p-3 dark:border-zinc-700 dark:bg-zinc-950">
        {selectedFile ? (
          <div className="flex items-start gap-3">
            {/* PDF 图标 */}
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-red-50 dark:bg-red-950">
              <svg className="h-5 w-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {selectedFile.name}
              </p>
              <p className="text-xs text-zinc-400">
                {textLength > 0
                  ? `已提取 ${textLength.toLocaleString()} 个字符`
                  : uploadStatus === "uploading"
                    ? "正在解析..."
                    : "解析中..."}
              </p>
              {/* 文件大小 */}
              <p className="text-xs text-zinc-400">
                {(selectedFile.size / 1024).toFixed(0)} KB
              </p>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-zinc-100 dark:bg-zinc-800">
              <svg className="h-5 w-5 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
            </div>
            <p className="text-xs text-zinc-400">暂无已上传的资料</p>
          </div>
        )}
      </div>
    </aside>
  );
}
