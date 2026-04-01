import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { HistoryStats } from '../types';

interface HistoryGraphProps {
  stats: HistoryStats[];
}

export default function HistoryGraph({ stats }: HistoryGraphProps) {
  if (stats.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">History</h3>
        <p className="text-gray-500 text-center py-8">No completed runs yet</p>
      </div>
    );
  }

  // Format data for chart
  const chartData = stats.map((stat) => ({
    date: new Date(stat.created_at).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    }),
    songs: stat.songs_count,
    albums: stat.albums_count,
  }));

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">History (Last {stats.length} Runs)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="songs"
            stroke="#f97316"
            strokeWidth={2}
            name="Songs"
            dot={{ fill: '#f97316' }}
          />
          <Line
            type="monotone"
            dataKey="albums"
            stroke="#3b82f6"
            strokeWidth={2}
            name="Albums"
            dot={{ fill: '#3b82f6' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
