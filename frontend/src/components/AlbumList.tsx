import { Album } from '../types';

interface AlbumListProps {
  albums: Album[];
}

export default function AlbumList({ albums }: AlbumListProps) {
  const getLikedBadge = (liked: string) => {
    if (liked === 'yes') {
      return <span className="text-green-600">✓ Liked</span>;
    } else if (liked === 'failed') {
      return <span className="text-red-600">✗ Failed</span>;
    }
    return <span className="text-gray-400">-</span>;
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Title
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Type
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Artist
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Tracks
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Liked
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Link
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {albums.map((album) => (
            <tr key={album.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm text-gray-900">
                {album.title}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                  {album.playlist_type}
                </span>
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {album.uploader}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {album.track_count}
              </td>
              <td className="px-4 py-3 text-sm">
                {getLikedBadge(album.liked)}
              </td>
              <td className="px-4 py-3 text-sm">
                <a
                  href={album.permalink_url}
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
