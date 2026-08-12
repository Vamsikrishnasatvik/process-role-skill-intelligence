import Link from "next/link";
import {
  getAIOpportunity,
  getAIOpportunityRoles,
  getAIOpportunitySkills,
} from "../../../lib/api";

type PageProps = {
  params: {
    id: string;
  };
};

export default async function AIOpportunityPage({
  params,
}: PageProps) {
  const [opportunity, roles, skills] = await Promise.all([
    getAIOpportunity(params.id),
    getAIOpportunityRoles(params.id),
    getAIOpportunitySkills(params.id),
  ]);

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/ai-opportunities"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Back to AI opportunities
        </Link>

        <section className="mt-6 rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
          <span className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
            AI Opportunity
          </span>

          <h1 className="mt-4 text-3xl font-bold text-zinc-900">
            {opportunity.name}
          </h1>

          <p className="mt-4 max-w-3xl leading-7 text-zinc-600">
            {opportunity.description || "No description available."}
          </p>

          {Object.keys(opportunity.metadata).length > 0 && (
            <div className="mt-6">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
                Opportunity Metadata
              </h2>

              <div className="mt-3 flex flex-wrap gap-2">
                {Object.entries(opportunity.metadata).map(
                  ([key, value]) => (
                    <span
                      key={key}
                      className="rounded-lg bg-zinc-100 px-3 py-2 text-sm text-zinc-700"
                    >
                      <span className="font-medium">{key}:</span>{" "}
                      {String(value)}
                    </span>
                  )
                )}
              </div>
            </div>
          )}
        </section>

        <section className="mt-8">
          <h2 className="text-2xl font-bold text-zinc-900">
            Impacted Roles
          </h2>

          <p className="mt-2 text-zinc-600">
            Enterprise roles affected by this AI opportunity.
          </p>

          {roles.length === 0 ? (
            <div className="mt-4 rounded-xl border border-zinc-200 bg-white p-6">
              <p className="text-zinc-600">
                No impacted roles found.
              </p>
            </div>
          ) : (
            <div className="mt-5 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {roles.map((role) => (
                <Link
                  key={role.id}
                  href={`/roles/${role.id}`}
                  className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                  <h3 className="text-lg font-semibold text-zinc-900">
                    {role.name}
                  </h3>

                  <p className="mt-3 text-sm leading-6 text-zinc-600">
                    {role.description ||
                      "No description available."}
                  </p>

                  <div className="mt-4 text-sm font-medium text-blue-600">
                    View role →
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="mt-10">
          <h2 className="text-2xl font-bold text-zinc-900">
            Impacted Skills
          </h2>

          <p className="mt-2 text-zinc-600">
            Skills associated with this AI opportunity.
          </p>

          {skills.length === 0 ? (
            <div className="mt-4 rounded-xl border border-zinc-200 bg-white p-6">
              <p className="text-zinc-600">
                No impacted skills found.
              </p>
            </div>
          ) : (
            <div className="mt-5 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {skills.map((skill) => (
                <Link
                  key={skill.id}
                  href={`/skills/${skill.id}`}
                  className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                  <h3 className="text-lg font-semibold text-zinc-900">
                    {skill.name}
                  </h3>

                  <p className="mt-3 text-sm leading-6 text-zinc-600">
                    {skill.description ||
                      "No description available."}
                  </p>

                  <div className="mt-4 text-sm font-medium text-blue-600">
                    View skill →
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}