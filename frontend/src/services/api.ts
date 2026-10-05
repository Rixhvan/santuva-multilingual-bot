import { ChatResponse, BenchmarkMetric } from '../models/types';

const API_BASE = '/api';

export const chatApi = {
  async sendMessage(text: string, conversationId = 'default', selectedLanguage?: string): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        conversation_id: conversationId,
        user_selected_language: selectedLanguage || null,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Network request failed' }));
      throw new Error(err.detail || 'Failed to send message');
    }

    return res.json();
  },

  async resetConversation(conversationId = 'default'): Promise<{ status: string }> {
    const res = await fetch(`${API_BASE}/reset?session_id=${conversationId}`, {
      method: 'POST',
    });
    return res.json();
  },

  async getInfo(): Promise<any> {
    const res = await fetch(`${API_BASE}/info`);
    return res.json();
  },

  async getEvaluationMetrics(): Promise<{ status: string; metrics: BenchmarkMetric[] }> {
    const res = await fetch(`${API_BASE}/evaluate`);
    if (!res.ok) {
      throw new Error('Failed to load evaluation metrics');
    }
    return res.json();
  }
};
