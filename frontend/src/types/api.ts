export interface AnomalyEvent {
  id: string;
  timestamp?: string;
  is_alert?: boolean;
  alert_type?: string;
  alert_level?: string;
  alert_title?: string;
  alert_message?: string;
  user_id?: string;
  tags?: Record<string, any>;
  metrics?: Record<string, any>;
}

export interface AnomalyEventFilter {
  start_time?: string;
  end_time?: string;
  is_alert?: boolean;
  alert_type?: string;
  alert_level?: string;
  user_id?: string;
  limit?: number;
  offset?: number;
}

export interface AnomalyEventStats {
  total_events: number;
  alert_count: number;
  alert_by_type: Record<string, number>;
  alert_by_level: Record<string, number>;
}

export interface AlertTrend {
  time_range: string;
  alert_count: number;
  total_count: number;
  alert_rate: number;
}

export interface ServiceAlertSummary {
  service: string;
  total_alerts: number;
  critical_alerts: number;
  warning_alerts: number;
  last_alert_time?: string;
}

export interface DashboardOverview {
  total_events: number;
  total_alerts: number;
  alert_rate: number;
  alerts_by_type: Record<string, number>;
  alerts_by_level: Record<string, number>;
  recent_alerts: Array<Record<string, any>>;
  time_range: {
    start?: string;
    end?: string;
  };
}

export interface AlertTimelineResponse {
  timeline: AlertTrend[];
  total_alerts: number;
  peak_alert_time?: string;
}
