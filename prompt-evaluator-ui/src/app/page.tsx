'use client';
import { useEffect, useState } from "react";
import Link from "next/link";

interface TraceMetadata {
  use_case: string;
  resource_id: string;
  workflow_step: string;
  model_version: string;
  prompt_version: string;
}

interface AIModelConfig {
  id: number;
  name: string;
  temperature: number;
  created_at: string;
}

interface TraceData {
  id: number;
  prompt: string;
  generation: string;
  created_at: string;
  trace_metadata: TraceMetadata;
  ai_model_config: AIModelConfig;
}

export default function Home() {
  const [traces, setTraces] = useState<TraceData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTraces = async () => {
      try {
        // Adjust the API URL to match your backend endpoint
        const response = await fetch('http://127.0.0.1:8000/traces');
        if (!response.ok) {
          throw new Error('Failed to fetch trace data');
        }
        const data = await response.json();
        setTraces(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTraces();
  }, []);

  // Function to truncate prompt text for preview
  const truncatePrompt = (prompt: string, maxLength: number = 50) => {
    return prompt.length > maxLength
      ? prompt.substring(0, maxLength) + '...'
      : prompt;
  };

  // Format date to be more readable
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-black">Prompt Evaluator</h1>

      {isLoading && (
        <div className="flex justify-center">
          <p className="text-black">Loading traces...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-black px-4 py-3 rounded mb-4">
          <p>Error: {error}</p>
        </div>
      )}

      {!isLoading && !error && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-black uppercase tracking-wider">Use Case</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-black uppercase tracking-wider">Prompt Preview</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-black uppercase tracking-wider">Model Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-black uppercase tracking-wider">Timestamp</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {traces.length > 0 ? (
                traces.map((trace) => (
                  <tr key={trace.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-black">{trace.trace_metadata.use_case}</td>
                    <td className="px-6 py-4">
                      <Link href={`/traces/${trace.id}`} className="text-black hover:underline">
                        {truncatePrompt(trace.prompt)}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-black">{trace.ai_model_config.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-black">{formatDate(trace.created_at)}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="px-6 py-4 text-center text-black">
                    No traces found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}