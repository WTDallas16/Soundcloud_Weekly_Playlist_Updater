import { useState, useEffect } from 'react';
import { runsApi, historyApi, authApi } from '../services/api';
import { Run, HistoryStats, AuthStatus } from '../types';
import RunForm from './RunForm';
import RunResults from './RunResults';
import HistoryGraph from './HistoryGraph';
import RunHistoryTable from './RunHistoryTable';

export default function Dashboard() {
  const [currentRun, setCurrentRun] = useState<Run | null>(null);
  const [historyStats, setHistoryStats] = useState<HistoryStats[]>([]);
  const [pastRuns, setPastRuns] = useState<Run[]>([]);
  const [authStatus, setAuthStatus] = useState<AuthStatus | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  // Check auth status on mount
  useEffect(() => {
    checkAuthStatus();
    loadHistory();
    loadPastRuns();
  }, []);

  // Poll for run completion
  useEffect(() => {
    if (!currentRun || currentRun.status !== 'running') {
      setIsPolling(false);
      return;
    }

    setIsPolling(true);
    const interval = setInterval(async () => {
      try {
        const updatedRun = await runsApi.get(currentRun.id);
        setCurrentRun(updatedRun);

        if (updatedRun.status !== 'running') {
          setIsPolling(false);
          loadHistory();
          loadPastRuns();
        }
      } catch (error) {
        console.error('Failed to poll run status:', error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [currentRun]);

  const checkAuthStatus = async () => {
    try {
      const status = await authApi.getStatus();
      setAuthStatus(status);
    } catch (error) {
      console.error('Failed to check auth status:', error);
    }
  };

  const loadHistory = async () => {
    try {
      const stats = await historyApi.getStats(20);
      setHistoryStats(stats);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const loadPastRuns = async () => {
    try {
      const runs = await runsApi.list(20);
      setPastRuns(runs);
    } catch (error) {
      console.error('Failed to load past runs:', error);
    }
  };

  const handleRunCreated = async (runId: number) => {
    try {
      const run = await runsApi.get(runId);
      setCurrentRun(run);
    } catch (error) {
      console.error('Failed to fetch run:', error);
    }
  };

  const handleSelectRun = async (runId: number) => {
    try {
      const run = await runsApi.get(runId);
      setCurrentRun(run);
    } catch (error) {
      console.error('Failed to fetch run:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-900">
              SoundCloud Weekly Updater
            </h1>
            {authStatus && (
              <div className="flex items-center space-x-2">
                <span
                  className={`h-2 w-2 rounded-full ${
                    authStatus.authenticated ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
                <span className="text-sm text-gray-600">
                  {authStatus.authenticated ? 'Authenticated' : 'Not Authenticated'}
                </span>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-1">
            <RunForm onRunCreated={handleRunCreated} />
          </div>
          <div className="lg:col-span-2">
            {currentRun ? (
              <RunResults run={currentRun} />
            ) : (
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-500 text-center py-12">
                  No active run. Start a new run to see results.
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <HistoryGraph stats={historyStats} />
          <RunHistoryTable runs={pastRuns} onSelectRun={handleSelectRun} />
        </div>
      </main>
    </div>
  );
}
