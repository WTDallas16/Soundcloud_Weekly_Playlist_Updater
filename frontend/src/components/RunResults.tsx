import { Run } from '../types';
import SongList from './SongList';
import AlbumList from './AlbumList';

interface RunResultsProps {
  run: Run;
}

export default function RunResults({ run }: RunResultsProps) {
  const getStatusBadge = () => {
    const statusColors = {
      running: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    };

    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColors[run.status]}`}>
        {run.status.toUpperCase()}
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Status Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Run #{run.id}</h2>
          {getStatusBadge()}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Created</p>
            <p className="font-medium">{new Date(run.created_at).toLocaleString()}</p>
          </div>
          <div>
            <p className="text-gray-500">Hours Back</p>
            <p className="font-medium">{run.hours_back}</p>
          </div>
          {run.duration_seconds && (
            <div>
              <p className="text-gray-500">Duration</p>
              <p className="font-medium">{run.duration_seconds.toFixed(1)}s</p>
            </div>
          )}
          {run.status === 'running' && (
            <div className="col-span-2 md:col-span-1">
              <p className="text-blue-600 animate-pulse">Processing...</p>
            </div>
          )}
        </div>

        {run.error_message && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
            <p className="font-medium">Error:</p>
            <p>{run.error_message}</p>
          </div>
        )}
      </div>

      {/* Count Cards */}
      {run.status === 'completed' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Songs Found</p>
                <p className="text-3xl font-bold text-orange-600">{run.songs_count}</p>
              </div>
              <div className="text-4xl">🎵</div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Albums Found</p>
                <p className="text-3xl font-bold text-orange-600">{run.albums_count}</p>
              </div>
              <div className="text-4xl">💿</div>
            </div>
          </div>
        </div>
      )}

      {/* Songs Table */}
      {run.status === 'completed' && run.songs.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Songs</h3>
          <SongList songs={run.songs} />
        </div>
      )}

      {/* Albums Table */}
      {run.status === 'completed' && run.albums.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Albums</h3>
          <AlbumList albums={run.albums} />
        </div>
      )}
    </div>
  );
}
