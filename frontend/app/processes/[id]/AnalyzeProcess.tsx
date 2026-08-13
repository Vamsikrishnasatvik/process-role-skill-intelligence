"use client";

import { useState } from "react";
import {
  analyzeProcess,
  ProcessAnalysis,
} from "../../../lib/api";

type Props = {
  processId: string;
  name: string;
  description: string | null;
};

export default function AnalyzeProcess({
  processId,
  name,
  description,
}: Props) {
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] =
    useState<ProcessAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze() {
    setLoading(true);
    setError(null);

    try {
      const result = await analyzeProcess(processId, {
        name,
        description,
      });

      setAnalysis(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to analyze process."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full md:w-auto">
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full rounded-xl bg-zinc-900 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-50 md:w-auto"
      >
        {loading ? "Analyzing..." : "✨ Analyze with AI"}
      </button>

      {error && (
        <div className="mt-3 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {analysis && (
        <div className="mt-6 rounded-2xl border border-zinc-200 bg-zinc-50 p-5 md:w-[520px]">
          <div className="mb-5">
            <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
              AI Process Analysis
            </p>

            <h3 className="mt-1 text-lg font-bold text-zinc-900">
              {analysis.process_name}
            </h3>
          </div>

          <div className="space-y-4">
            {analysis.activities.map((activity, index) => (
              <div
                key={`${activity.name}-${index}`}
                className="rounded-xl border border-zinc-200 bg-white p-4"
              >
                <h4 className="font-semibold text-zinc-900">
                  {activity.name}
                </h4>

                {activity.description && (
                  <p className="mt-1 text-sm text-zinc-600">
                    {activity.description}
                  </p>
                )}

                <div className="mt-4 grid gap-4 sm:grid-cols-2">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                      Roles
                    </p>

                    <div className="mt-2 space-y-1">
                      {activity.roles.map((role) => (
                        <div
                          key={role.name}
                          className="rounded-lg bg-zinc-100 px-3 py-2 text-sm text-zinc-700"
                        >
                          {role.name}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                      Skills
                    </p>

                    <div className="mt-2 space-y-1">
                      {activity.skills.map((skill) => (
                        <div
                          key={skill.name}
                          className="rounded-lg bg-zinc-100 px-3 py-2 text-sm text-zinc-700"
                        >
                          {skill.name}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <p className="mt-4 text-xs text-zinc-400">
            Analysis is persisted into the intelligence graph.
          </p>
        </div>
      )}
    </div>
  );
}