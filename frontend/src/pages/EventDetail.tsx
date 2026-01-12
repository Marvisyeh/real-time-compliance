import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { eventsApi } from '@/api/client';
import type { AnomalyEvent } from '@/types/api';
import { format } from 'date-fns';
import { ArrowLeft, AlertTriangle } from 'lucide-react';

export default function EventDetail() {
  const { eventId } = useParams<{ eventId: string }>();
  const [event, setEvent] = useState<AnomalyEvent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (eventId) {
      loadEvent();
    }
  }, [eventId]);

  const loadEvent = async () => {
    if (!eventId) return;
    try {
      setLoading(true);
      setError(null);
      const data = await eventsApi.get(eventId);
      setEvent(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load event');
      console.error('Failed to load event:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAlertLevelColor = (level?: string) => {
    switch (level?.toUpperCase()) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'WARNING':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'INFO':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading event...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <Link
          to="/events"
          className="inline-flex items-center text-primary-600 hover:text-primary-900"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Events
        </Link>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error: {error}</p>
        </div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="space-y-4">
        <Link
          to="/events"
          className="inline-flex items-center text-primary-600 hover:text-primary-900"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Events
        </Link>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">Event not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link
        to="/events"
        className="inline-flex items-center text-primary-600 hover:text-primary-900"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Events
      </Link>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">Event Details</h2>
            {event.is_alert && (
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-red-600" />
                <span className="text-sm font-medium text-red-600">Alert</span>
              </div>
            )}
          </div>
        </div>

        <div className="px-6 py-4 space-y-6">
          {/* Basic Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h3>
            <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Event ID</dt>
                <dd className="mt-1 text-sm text-gray-900 font-mono">{event.id}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Timestamp</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {event.timestamp
                    ? format(new Date(event.timestamp), 'yyyy-MM-dd HH:mm:ss')
                    : 'N/A'}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Alert Type</dt>
                <dd className="mt-1 text-sm text-gray-900">{event.alert_type || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Alert Level</dt>
                <dd className="mt-1">
                  {event.alert_level ? (
                    <span
                      className={`inline-block px-3 py-1 text-xs font-semibold rounded-full border ${getAlertLevelColor(
                        event.alert_level
                      )}`}
                    >
                      {event.alert_level}
                    </span>
                  ) : (
                    <span className="text-sm text-gray-500">N/A</span>
                  )}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">User ID</dt>
                <dd className="mt-1 text-sm text-gray-900">{event.user_id || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Is Alert</dt>
                <dd className="mt-1">
                  <span
                    className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${
                      event.is_alert
                        ? 'bg-red-100 text-red-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {event.is_alert ? 'Yes' : 'No'}
                  </span>
                </dd>
              </div>
            </dl>
          </div>

          {/* Alert Information */}
          {(event.alert_title || event.alert_message) && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Alert Information</h3>
              <dl className="space-y-4">
                {event.alert_title && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Title</dt>
                    <dd className="mt-1 text-sm text-gray-900">{event.alert_title}</dd>
                  </div>
                )}
                {event.alert_message && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Message</dt>
                    <dd className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">
                      {event.alert_message}
                    </dd>
                  </div>
                )}
              </dl>
            </div>
          )}

          {/* Tags */}
          {event.tags && Object.keys(event.tags).length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Tags</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-sm text-gray-900 overflow-x-auto">
                  {JSON.stringify(event.tags, null, 2)}
                </pre>
              </div>
            </div>
          )}

          {/* Metrics */}
          {event.metrics && Object.keys(event.metrics).length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Metrics</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-sm text-gray-900 overflow-x-auto">
                  {JSON.stringify(event.metrics, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
