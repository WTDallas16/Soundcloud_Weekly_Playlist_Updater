import axios from 'axios';
import { Run, RunCreate, HistoryStats, AuthStatus } from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const runsApi = {
  create: async (data: RunCreate): Promise<Run> => {
    const response = await api.post<Run>('/runs/', data);
    return response.data;
  },

  get: async (runId: number): Promise<Run> => {
    const response = await api.get<Run>(`/runs/${runId}`);
    return response.data;
  },

  list: async (limit: number = 20): Promise<Run[]> => {
    const response = await api.get<Run[]>('/runs/', { params: { limit } });
    return response.data;
  },
};

export const historyApi = {
  getStats: async (limit: number = 20): Promise<HistoryStats[]> => {
    const response = await api.get<HistoryStats[]>('/history/stats', { params: { limit } });
    return response.data;
  },
};

export const authApi = {
  getStatus: async (): Promise<AuthStatus> => {
    const response = await api.get<AuthStatus>('/auth/status');
    return response.data;
  },
};

export const healthApi = {
  check: async (): Promise<{ status: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};
