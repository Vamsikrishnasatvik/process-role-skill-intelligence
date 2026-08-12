import Link from "next/link";
import { getSkills, type Skill } from "../../lib/api";

export default async function SkillsPage() {
  const skills = await getSkills();

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
            Skills
          </h1>

          <p className="mt-2 text-zinc-600">
            Enterprise skills connected to roles, processes, and activities.
          </p>
        </div>

        {skills.length === 0 ? (
          <div className="rounded-xl border border-zinc-200 bg-white p-6">
            <p className="text-zinc-600">No skills found.</p>
          </div>
        ) : (
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {skills.map((skill: Skill) => (
              <Link
                key={skill.id}
                href={`/skills/${skill.id}`}
                className="group rounded-xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
              >
                <h2 className="text-xl font-semibold text-zinc-900 group-hover:text-blue-600">
                  {skill.name}
                </h2>

                <p className="mt-3 text-sm leading-6 text-zinc-600">
                  {skill.description || "No description available."}
                </p>

                {Object.keys(skill.metadata).length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {Object.entries(skill.metadata).map(([key, value]) => (
                      <span
                        key={key}
                        className="rounded-full bg-zinc-100 px-3 py-1 text-xs text-zinc-600"
                      >
                        {key}: {String(value)}
                      </span>
                    ))}
                  </div>
                )}

                <div className="mt-5 text-sm font-medium text-blue-600">
                  View skill →
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}