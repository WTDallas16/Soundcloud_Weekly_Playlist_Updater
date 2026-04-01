export interface Song {
  id: number;
  run_id: number;
  track_id: string;
  track_title: string;
  track_permalink_url: string;
  uploader_username: string;
  uploaded_at?: string;
  activity_created_at?: string;
}

export interface Album {
  id: number;
  run_id: number;
  playlist_id: string;
  title: string;
  playlist_type: string;
  permalink_url: string;
  uploader: string;
  track_count: number;
  activity_created_at?: string;
  liked: string;
}

export interface Run {
  id: number;
  created_at: string;
  hours_back: number;
  start_time?: string;
  end_time?: string;
  status: 'running' | 'completed' | 'failed';
  songs_count: number;
  albums_count: number;
  error_message?: string;
  duration_seconds?: number;
  songs: Song[];
  albums: Album[];
}

export interface RunCreate {
  hours_back: number;
}

export interface HistoryStats {
  run_id: number;
  created_at: string;
  songs_count: number;
  albums_count: number;
}

export interface AuthStatus {
  authenticated: boolean;
  token_expires_at?: string;
  message?: string;
}
