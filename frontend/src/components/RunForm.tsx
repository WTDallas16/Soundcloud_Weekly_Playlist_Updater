import { useState } from 'react';
import { runsApi } from '../services/api';

interface RunFormProps {
  onRunCreated: (runId: number) => void;
}

export default function RunForm({ onRunCreated }: RunFormProps) {
  const [hoursBack, setHoursBack] = useState<number>(168); // 7 days default
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const run = await runsApi.create({ hours_back: hoursBack });
      onRunCreated(run.id);
    } catch (error) {
      console.error('Failed to create run:', error);
      alert('Failed to start run. Check console for details.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">New Run</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="hoursBack" className="block text-sm font-medium text-gray-700 mb-1">
            Hours to Look Back
          </label>
          <input
            type="number"
            id="hoursBack"
            value={hoursBack}
            onChange={(e) => setHoursBack(Number(e.target.value))}
            min="1"
            step="1"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
            disabled={isSubmitting}
          />
          <p className="mt-1 text-xs text-gray-500">
            Default: 168 hours (7 days)
          </p>
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-orange-500 text-white py-2 px-4 rounded-md hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isSubmitting ? 'Starting...' : 'Start Run'}
        </button>
      </form>
    </div>
  );
}
