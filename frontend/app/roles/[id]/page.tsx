import Link from "next/link";
import {
  getRole,
  getRoleSkills,
  getRoleProcesses,
  type Skill,
  type Process,
} from "../../../lib/api";

type Props = {
  params: {
    id: string;
  };
};

export default async function RoleDetailPage({ params }: Props) {
  const [role, skills, processes] = await Promise.all([
    getRole(params.id),
    getRoleSkills(params.id),
    getRoleProcesses(params.id),
  ]);

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/roles"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Back to roles
        </Link>

        {/* Role Header */}
        <section className="mt-6 rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
          <div className="flex items-start justify-between gap-6">
            <div>
              <p className="text-sm font-medium text-blue-600">
                Enterprise Role
              </p>

              <h1 className="mt-2 text-3xl font-bold text-zinc-900">
                {role.name}
              </h1>

              <p className="mt-4 max-w-3xl leading-7 text-zinc-600">
                {role.description || "No description available."}
              </p>
            </div>

            <div className="rounded-xl bg-zinc-100 px-4 py-3 text-center">
              <p className="text-2xl font-bold text-zinc-900">
                {skills.length}
              </p>
              <p className="text-xs text-zinc-500">Skills</p>
            </div>
          </div>
        </section>

        {/* Skills */}
        <section className="mt-8">
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-zinc-900">
              Skills
            </h2>

            <p className="mt-1 text-sm text-zinc-600">
              Skills associated with this role.
            </p>
          </div>

          {skills.length === 0 ? (
            <div className="rounded-xl border border-zinc-200 bg-white p-6">
              <p className="text-zinc-600">
                No skills assigned to this role.
              </p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {skills.map((skill: Skill) => (
                <Link
                  key={skill.id}
                  href={`/skills/${skill.id}`}
                  className="rounded-xl border border-zinc-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                  <h3 className="font-semibold text-zinc-900">
                    {skill.name}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-zinc-600">
                    {skill.description || "No description available."}
                  </p>
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
              Business processes connected to this role through activities.
            </p>
          </div>

          {processes.length === 0 ? (
            <div className="rounded-xl border border-zinc-200 bg-white p-6">
              <p className="text-zinc-600">
                No processes associated with this role.
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