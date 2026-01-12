import axios from 'axios';
import type {
  AnomalyEvent,
  AnomalyEventFilter,
  AnomalyEventStats,
  DashboardOverview,
  AlertTimelineResponse,
  ServiceAlertSummary,
} from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Events API
export const eventsApi = {
  list: async (filters?: AnomalyEventFilter): Promise<AnomalyEvent[]> => {
    const params = new URLSearchParams();
    if (filters?.start_time) params.append('start_time', filters.start_time);
    if (filters?.end_time) params.append('end_time', filters.end_time);
    if (filters?.is_alert !== undefined) params.append('is_alert', String(filters.is_alert));
    if (filters?.alert_type) params.append('alert_type', filters.alert_type);
    if (filters?.alert_level) params.append('alert_level', filters.alert_level);
    if (filters?.user_id) params.append('user_id', filters.user_id);
    if (filters?.limit) params.append('limit', String(filters.limit));
    if (filters?.offset) params.append('offset', String(filters.offset));

    const response = await client.get<AnomalyEvent[]>(`/events?${params.toString()}`);
    return response.data;
  },

  get: async (eventId: string): Promise<AnomalyEvent> => {
    const response = await client.get<AnomalyEvent>(`/events/${eventId}`);
    return response.data;
  },

  getStats: async (startTime?: string, endTime?: string): Promise<AnomalyEventStats> => {
    const params = new URLSearchParams();
    if (startTime) params.append('start_time', startTime);
    if (endTime) params.append('end_time', endTime);

    const response = await client.get<AnomalyEventStats>(
      `/events/stats/summary?${params.toString()}`
    );
    return response.data;
  },
};

// Dashboard API
export const dashboardApi = {
  getOverview: async (startTime?: string, endTime?: string): Promise<DashboardOverview> => {
    const params = new URLSearchParams();
    if (startTime) params.append('start_time', startTime);
    if (endTime) params.append('end_time', endTime);

    const response = await client.get<DashboardOverview>(
      `/dashboard/overview?${params.toString()}`
    );
    return response.data;
  },

  getTimeline: async (
    startTime?: string,
    endTime?: string,
    groupBy: 'hour' | 'day' | 'week' = 'hour',
    alertType?: string
  ): Promise<AlertTimelineResponse> => {
    const params = new URLSearchParams();
    if (startTime) params.append('start_time', startTime);
    if (endTime) params.append('end_time', endTime);
    params.append('group_by', groupBy);
    if (alertType) params.append('alert_type', alertType);

    const response = await client.get<AlertTimelineResponse>(
      `/dashboard/timeline?${params.toString()}`
    );
    return response.data;
  },

  getServices: async (startTime?: string, endTime?: string): Promise<ServiceAlertSummary[]> => {
    const params = new URLSearchParams();
    if (startTime) params.append('start_time', startTime);
    if (endTime) params.append('end_time', endTime);

    const response = await client.get<ServiceAlertSummary[]>(
      `/dashboard/services?${params.toString()}`
    );
    return response.data;
  },
};

// Health check
export const healthApi = {
  check: async (): Promise<{ status: string; service: string; version: string }> => {
    const response = await client.get('/health');
    return response.data;
  },
};
