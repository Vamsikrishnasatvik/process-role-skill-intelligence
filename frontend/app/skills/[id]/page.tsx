import Link from "next/link";
import {
  getSkill,
  getSkillRoles,
  getSkillProcesses,
  type Role,
  type Process,
} from "../../../lib/api";

type Props = {
  params: {
    id: string;
  };
};

export default async function SkillDetailPage({ params }: Props) {
  const [skill, roles, processes] = await Promise.all([
    getSkill(params.id),
    getSkillRoles(params.id),
    getSkillProcesses(params.id),
  ]);

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/skills"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Back to skills
        </Link>

        {/* Skill Header */}
        <section className="mt-6 rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
          <p className="text-sm font-medium text-blue-600">
            Enterprise Skill
          </p>

          <h1 className="mt-2 text-3xl font-bold text-zinc-900">
            {skill.name}
          </h1>

          <p className="mt-4 max-w-3xl leading-7 text-zinc-600">
            {skill.description || "No description available."}
          </p>

          {Object.keys(skill.metadata).length > 0 && (
            <div className="mt-5 flex flex-wrap gap-2">
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
        </section>

        {/* Roles */}
        <section className="mt-8">
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-zinc-900">
              Roles
            </h2>

            <p className="mt-1 text-sm text-zinc-600">
              Enterprise roles associated with this skill.
            </p>
          </div>

          {roles.length === 0 ? (
            <div className="rounded-xl border border-zinc-200 bg-white p-6">
              <p className="text-zinc-600">
                No roles associated with this skill.
              </p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {roles.map((role: Role) => (
                <Link
                  key={role.id}
                  href={`/roles/${role.id}`}
                  className="group rounded-xl border border-zinc-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                  <h3 className="text-lg font-semibold text-zinc-900 group-hover:text-blue-600">
                    {role.name}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-zinc-600">
                    {role.description || "No description available."}
                  </p>

                  <div className="mt-4 text-sm font-medium text-blue-600">
                    View role →
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>

        {/* Processes */}
        <section className="mt-10">
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-zinc-900">
              Processes
            </h2>

            <p className="mt-1 text-sm text-zinc-600">
              Business processes connected to this skill.
            </p>
          </div>

          {processes.length === 0 ? (
            <div className="rounded-xl border border-zinc-200 bg-white p-6">
              <p className="text-zinc-600">
                No processes associated with this skill.
              </p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {processes.map((process: Process) => (
                <div
                  key={process.id}
                  className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm"
                >
                  <h3 className="text-lg font-semibold text-zinc-900">
                    {process.name}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-zinc-600">
                    {process.description || "No description available."}
                  </p>

                  {Object.keys(process.metadata).length > 0 && (
                    <div className="mt-4 flex flex-wrap gap-2">
                      {Object.entries(process.metadata).map(
                        ([key, value]) => (
                          <span
                            key={key}
                            className="rounded-full bg-zinc-100 px-3 py-1 text-xs text-zinc-600"
                          >
                            {key}: {String(value)}
                          </span>
                        )
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}