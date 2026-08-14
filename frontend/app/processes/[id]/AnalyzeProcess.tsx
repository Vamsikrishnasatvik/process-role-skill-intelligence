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

  const activityCount = analysis?.activities.length ?? 0;

  const roleCount =
    analysis?.activities.reduce(
      (total, activity) => total + activity.roles.length,
      0
    ) ?? 0;

  const skillCount =
    analysis?.activities.reduce(
      (total, activity) => total + activity.skills.length,
      0
    ) ?? 0;

  const opportunityCount =
    analysis?.activities.reduce(
      (total, activity) =>
        total + (activity.ai_opportunities?.length ?? 0),
      0
    ) ?? 0;

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
        <div className="mt-6 rounded-2xl border border-zinc-200 bg-zinc-50 p-5 md:w-[620px]">
          {/* Success message */}
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
            <div className="flex items-center gap-2">
              <span className="text-lg">✓</span>

              <div>
                <p className="font-semibold text-emerald-900">
                  AI Analysis Complete
                </p>

                <p className="mt-1 text-xs text-emerald-700">
                  Analysis has been persisted to the intelligence graph.
                </p>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="mt-5">
            <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
              Analysis Summary
            </p>

            <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
              <div className="rounded-xl border border-zinc-200 bg-white p-3">
                <p className="text-2xl font-bold text-zinc-900">
                  {activityCount}
                </p>
                <p className="text-xs text-zinc-500">
                  Activities
                </p>
              </div>

              <div className="rounded-xl border border-zinc-200 bg-white p-3">
                <p className="text-2xl font-bold text-zinc-900">
                  {roleCount}
                </p>
                <p className="text-xs text-zinc-500">
                  Roles
                </p>
              </div>

              <div className="rounded-xl border border-zinc-200 bg-white p-3">
                <p className="text-2xl font-bold text-zinc-900">
                  {skillCount}
                </p>
                <p className="text-xs text-zinc-500">
                  Skills
                </p>
              </div>

              <div className="rounded-xl border border-zinc-200 bg-white p-3">
                <p className="text-2xl font-bold text-zinc-900">
                  {opportunityCount}
                </p>
                <p className="text-xs text-zinc-500">
                  AI Opportunities
                </p>
              </div>
            </div>
          </div>

          {/* Generated analysis */}
          <div className="mt-6">
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

                  {/* AI Opportunities */}
                  {activity.ai_opportunities &&
                    activity.ai_opportunities.length > 0 && (
                      <div className="mt-4">
                        <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                          AI Opportunities
                        </p>

                        <div className="mt-2 space-y-1">
                          {activity.ai_opportunities.map(
                            (opportunity) => (
                              <div
                                key={opportunity.name}
                                className="rounded-lg bg-zinc-100 px-3 py-2 text-sm text-zinc-700"
                              >
                                {opportunity.name}
                              </div>
                            )
                          )}
                        </div>
                      </div>
                    )}
                </div>
              ))}
            </div>
          </div>

          <p className="mt-5 text-xs text-zinc-400">
            Generated insights are structured and persisted into the
            enterprise intelligence graph.
          </p>
        </div>
      )}
    </div>
  );
}