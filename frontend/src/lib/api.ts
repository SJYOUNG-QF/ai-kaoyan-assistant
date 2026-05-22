/**
 * API 层
 * 集中管理所有后端请求，避免 URL 散落在组件中
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function uploadPdf(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/api/pdf/upload`, {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  if (!res.ok || !data.success) {
    throw new Error(data.detail || "上传失败");
  }

  return data as {
    success: boolean;
    filename: string;
    size: number;
    text_length: number;
    text_preview: string;
    message: string;
  };
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export async function askQuestion(
  question: string,
  filename: string,
  history: ChatMessage[] = [],
  useTestText: boolean = false,
) {
  const res = await fetch(`${API_BASE}/api/chat/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, filename, history, use_test_text: useTestText }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "请求失败");
  }

  return data as {
    answer: string;
    text_length: number;
  };
}
