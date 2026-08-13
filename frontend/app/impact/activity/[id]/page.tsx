import Link from "next/link";
import {
  getActivityImpact,
  getEvidence,
} from "../../../../lib/api";

type PageProps = {
  params: {
    id: string;
  };
  searchParams?: {
    q?: string;
  };
};

export default async function ActivityImpactPage({
  params,
  searchParams,
}: PageProps) {
  const [data, evidence] = await Promise.all([
    getActivityImpact(params.id),
    getEvidence("activity", params.id),
  ]);

  const query = searchParams?.q?.trim().toLowerCase() ?? "";

  const filteredEvidence = query
    ? evidence.filter((item) => {
        const searchableText = [
          item.source_title,
          item.source_type,
          item.snippet ?? "",
          item.metadata
            ? Object.values(item.metadata).join(" ")
            : "",
        ]
          .join(" ")
          .toLowerCase();

        return searchableText.includes(query);
      })
    : evidence;

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-7xl">

        {/* Back */}
        <div className="mb-6">
          <Link
            href="/"
            className="text-sm font-medium text-zinc-500 hover:text-zinc-900"
          >
            ← Back to Intelligence Graph
          </Link>
        </div>

        {/* Header */}
        <header className="mb-8">
          <div className="mb-3 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-700">
              Impact Explorer
            </span>

            <span className="rounded-full bg-zinc-200 px-3 py-1 text-xs font-medium text-zinc-600">
              Activity
            </span>
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-zinc-900">
            {data.activity.name}
          </h1>

          <p className="mt-3 max-w-4xl text-zinc-600">
            {data.activity.description}
          </p>
        </header>

        {/* Activity + Process */}
        <section className="mb-8 grid gap-6 md:grid-cols-2">

          <div className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-400">
              Activity
            </p>

            <h2 className="text-xl font-semibold text-zinc-900">
              {data.activity.name}
            </h2>

            <p className="mt-3 text-sm leading-6 text-zinc-600">
              {data.activity.description}
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              {Object.entries(data.activity.metadata).map(
                ([key, value]) => (
                  <span
                    key={key}
                    className="rounded-md bg-zinc-100 px-3 py-1.5 text-xs text-zinc-600"
                  >
                    <span className="font-medium">{key}:</span>{" "}
                    {String(value)}
                  </span>
                )
              )}
            </div>
          </div>

          <div className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-400">
              Process
            </p>

            <h2 className="text-xl font-semibold text-zinc-900">
              {data.process.name}
            </h2>

            <p className="mt-3 text-sm leading-6 text-zinc-600">
              {data.process.description}
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              {Object.entries(data.process.metadata).map(
                ([key, value]) => (
                  <span
                    key={key}
                    className="rounded-md bg-zinc-100 px-3 py-1.5 text-xs text-zinc-600"
                  >
                    <span className="font-medium">{key}:</span>{" "}
                    {String(value)}
                  </span>
                )
              )}
            </div>
          </div>
        </section>

        {/* AI Opportunities */}
        <section className="mb-8">
          <div className="mb-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
              AI Opportunities
            </p>

            <h2 className="mt-1 text-2xl font-bold text-zinc-900">
              AI interventions
            </h2>
          </div>

          <div className="space-y-4">
            {data.ai_opportunities.map((opportunity) => (
              <div
                key={opportunity.id}
                className="rounded-xl border border-indigo-100 bg-white p-6 shadow-sm"
              >
                <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-zinc-900">
                      {opportunity.name}
                    </h3>

                    <p className="mt-2 max-w-4xl text-sm leading-6 text-zinc-600">
                      {opportunity.description}
                    </p>
                  </div>

                  <Link
                    href={`/ai-opportunities/${opportunity.id}`}
                    className="shrink-0 rounded-lg border border-zinc-200 px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50"
                  >
                    View opportunity →
                  </Link>
                </div>

                <div className="mt-5 flex flex-wrap gap-2">
                  {Object.entries(opportunity.metadata).map(
                    ([key, value]) => (
                      <span
                        key={key}
                        className="rounded-md bg-zinc-100 px-3 py-1.5 text-xs text-zinc-600"
                      >
                        <span className="font-medium">{key}:</span>{" "}
                        {String(value)}
                      </span>
                    )
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Impact Assessment */}
        <section className="mb-8">
          <div className="mb-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
              Impact Assessment
            </p>

            <h2 className="mt-1 text-2xl font-bold text-zinc-900">
              How AI changes this activity
            </h2>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-zinc-200 bg-white p-5 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                Impact Type
              </p>

              <p className="mt-2 text-lg font-semibold capitalize text-zinc-900">
                {data.impact.type}
              </p>
            </div>

            <div className="rounded-xl border border-zinc-200 bg-white p-5 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                Automation Level
              </p>

              <div className="mt-2 flex flex-wrap gap-2">
                {data.impact.automation_levels.map((level) => (
                  <span
                    key={level}
                    className="rounded-full bg-amber-100 px-3 py-1 text-sm font-medium text-amber-700"
                  >
                    {level.replaceAll("_", " ")}
                  </span>
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-zinc-200 bg-white p-5 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                AI Pattern
              </p>

              <div className="mt-2 flex flex-wrap gap-2">
                {data.impact.ai_patterns.map((pattern) => (
                  <span
                    key={pattern}
                    className="rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-700"
                  >
                    {pattern.replaceAll("_", " ")}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Roles */}
        <section className="mb-8">
          <div className="mb-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
              Impacted Roles
            </p>

            <h2 className="mt-1 text-2xl font-bold text-zinc-900">
              Roles
            </h2>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {data.impacted_roles.map((role) => (
              <Link
                key={role.id}
                href={`/roles/${role.id}`}
                className="group rounded-xl border border-zinc-200 bg-white p-5 shadow-sm transition hover:border-indigo-300 hover:shadow-md"
              >
                <h3 className="font-semibold text-zinc-900 group-hover:text-indigo-600">
                  {role.name}
                </h3>

                <p className="mt-2 text-sm leading-6 text-zinc-600">
                  {role.description}
                </p>

                <span className="mt-4 inline-block text-sm font-medium text-indigo-600">
                  View role →
                </span>
              </Link>
            ))}
          </div>
        </section>

        {/* Skills */}
        <section className="mb-8">
          <div className="mb-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
              Impacted Skills
            </p>

            <h2 className="mt-1 text-2xl font-bold text-zinc-900">
              Skills
            </h2>
          </div>

          <div className="flex flex-wrap gap-3">
            {data.impacted_skills.map((skill) => (
              <Link
                key={skill.id}
                href={`/skills/${skill.id}`}
                className="rounded-lg border border-zinc-200 bg-white px-4 py-3 text-sm font-medium text-zinc-700 shadow-sm transition hover:border-indigo-300 hover:text-indigo-600"
              >
                {skill.name}
              </Link>
            ))}
          </div>
        </section>

        {/* Workforce Transformation */}
        <section className="mb-8">
          <div className="mb-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
              Workforce Transformation
            </p>

            <h2 className="mt-1 text-2xl font-bold text-zinc-900">
              What changes?
            </h2>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
              <h3 className="font-semibold text-zinc-900">
                Role Change
              </h3>

              <p className="mt-3 text-sm leading-6 text-zinc-600">
                {data.impact.role_change}
              </p>
            </div>

            <div className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
              <h3 className="font-semibold text-zinc-900">
                Skill Change
              </h3>

              <p className="mt-3 text-sm leading-6 text-zinc-600">
                {data.impact.skill_change}
              </p>
            </div>

            <div className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
              <h3 className="font-semibold text-zinc-900">
                Future State
              </h3>

              <p className="mt-3 text-sm leading-6 text-zinc-600">
                {data.impact.future_change}
              </p>
            </div>
          </div>
        </section>

        {/* Evidence */}
        <section className="mb-8">
          <div className="mb-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                Evidence
              </p>

              <h2 className="mt-1 text-2xl font-bold text-zinc-900">
                Supporting sources
              </h2>

              <p className="mt-1 text-sm text-zinc-500">
                {filteredEvidence.length} of {evidence.length} sources
              </p>
            </div>

            {/* Search */}
            <form
              method="GET"
              className="flex w-full gap-2 md:w-auto"
            >
              <input
                type="search"
                name="q"
                defaultValue={searchParams?.q ?? ""}
                placeholder="Search evidence..."
                className="w-full rounded-lg border border-zinc-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 md:w-72"
              />

              <button
                type="submit"
                className="rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-zinc-700"
              >
                Search
              </button>

              {query && (
                <Link
                  href={`/impact/activity/${params.id}`}
                  className="rounded-lg border border-zinc-300 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 hover:bg-zinc-50"
                >
                  Clear
                </Link>
              )}
            </form>
          </div>

          {filteredEvidence.length === 0 ? (
            <div className="rounded-xl border border-dashed border-zinc-300 bg-white p-10 text-center">
              <h3 className="font-semibold text-zinc-900">
                No evidence found
              </h3>

              <p className="mt-2 text-sm text-zinc-500">
                Try a different search term.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredEvidence.map((item) => (
                <article
                  key={item.id}
                  className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm"
                >
                  <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-zinc-900">
                        {item.source_title}
                      </h3>

                      <div className="mt-2 flex flex-wrap items-center gap-2">
                        <span className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-600">
                          {item.source_type}
                        </span>

                        {typeof item.metadata.evidence_level ===
                          "string" && (
                          <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
                            {item.metadata.evidence_level}
                          </span>
                        )}
                      </div>
                    </div>

                    {item.source_url && (
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="shrink-0 text-sm font-semibold text-indigo-600 hover:text-indigo-800"
                      >
                        View source →
                      </a>
                    )}
                  </div>

                  {item.snippet && (
                    <p className="mt-4 text-sm leading-6 text-zinc-600">
                      {item.snippet}
                    </p>
                  )}

                  <p className="mt-4 text-xs text-zinc-400">
                    Retrieved{" "}
                    {new Date(item.retrieved_at).toLocaleDateString()}
                  </p>
                </article>
              ))}
            </div>
          )}
        </section>

        {/* Navigation */}
        <footer className="flex flex-wrap gap-3 border-t border-zinc-200 pt-6">
          <Link
            href="/roles"
            className="rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 hover:bg-zinc-50"
          >
            Browse Roles
          </Link>

          <Link
            href="/skills"
            className="rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 hover:bg-zinc-50"
          >
            Browse Skills
          </Link>

          <Link
            href="/ai-opportunities"
            className="rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 hover:bg-zinc-50"
          >
            AI Opportunities
          </Link>
        </footer>
      </div>
    </main>
  );
}