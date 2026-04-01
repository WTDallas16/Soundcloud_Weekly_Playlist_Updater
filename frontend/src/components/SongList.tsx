import { Song } from '../types';

interface SongListProps {
  songs: Song[];
}

export default function SongList({ songs }: SongListProps) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Track
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Artist
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Link
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {songs.map((song) => (
            <tr key={song.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm text-gray-900">
                {song.track_title}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {song.uploader_username}
              </td>
              <td className="px-4 py-3 text-sm">
                <a
                  href={song.track_permalink_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-orange-600 hover:text-orange-800 hover:underline"
                >
                  Open in SoundCloud →
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
