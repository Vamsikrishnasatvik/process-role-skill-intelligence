import Link from "next/link";
import { getAIOpportunities } from "../../lib/api";

export default async function AIOpportunitiesPage() {
  const opportunities = await getAIOpportunities();

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8">
          <Link
            href="/"
            className="text-sm text-zinc-500 hover:text-zinc-900"
          >
            ← Back to home
          </Link>

          <h1 className="mt-4 text-3xl font-bold text-zinc-900">
            AI Opportunities
          </h1>

          <p className="mt-2 text-zinc-600">
            Enterprise AI opportunities connected to activities, roles, and
            skills.
          </p>
        </div>

        {opportunities.length === 0 ? (
          <div className="rounded-xl border border-zinc-200 bg-white p-6">
            <p className="text-zinc-600">
              No AI opportunities found.
            </p>
          </div>
        ) : (
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {opportunities.map((opportunity) => (
              <Link
                key={opportunity.id}
                href={`/ai-opportunities/${opportunity.id}`}
                className="group rounded-xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
              >
                <div className="mb-4">
                  <span className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
                    AI Opportunity
                  </span>
                </div>

                <h2 className="text-xl font-semibold text-zinc-900 group-hover:text-blue-600">
                  {opportunity.name}
                </h2>

                <p className="mt-3 text-sm leading-6 text-zinc-600">
                  {opportunity.description ||
                    "No description available."}
                </p>

                {Object.keys(opportunity.metadata).length > 0 && (
                  <div className="mt-5 flex flex-wrap gap-2">
                    {Object.entries(opportunity.metadata).map(
                      ([key, value]) => (
                        <span
                          key={key}
                          className="rounded-md bg-zinc-100 px-2 py-1 text-xs text-zinc-600"
                        >
                          {key}: {String(value)}
                        </span>
                      )
                    )}
                  </div>
                )}

                <div className="mt-6 text-sm font-medium text-blue-600">
                  View opportunity →
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}