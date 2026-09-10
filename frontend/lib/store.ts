import { SessionData } from './api';

export function saveSession(sessionId: string, data: SessionData): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('impactx_session_id', sessionId);
    localStorage.setItem('impactx_session_data', JSON.stringify(data));
  }
}

export function loadSession(): { sessionId: string; data: SessionData } | null {
  if (typeof window !== 'undefined') {
    const sessionId = localStorage.getItem('impactx_session_id');
    const dataStr = localStorage.getItem('impactx_session_data');
    if (sessionId && dataStr) {
      try {
        return { sessionId, data: JSON.parse(dataStr) };
      } catch (e) {
        return null;
      }
    }
  }
  return null;
}

export function clearSession(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('impactx_session_id');
    localStorage.removeItem('impactx_session_data');
  }
}
