import Link from "next/link";
import { getRoles } from "../../lib/api";

export default async function RolesPage() {
  const roles = await getRoles();

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
            Roles
          </h1>

          <p className="mt-2 text-zinc-600">
            Enterprise roles connected to processes, activities, and skills.
          </p>
        </div>

        {roles.length === 0 ? (
          <div className="rounded-xl border border-zinc-200 bg-white p-6">
            <p className="text-zinc-600">No roles found.</p>
          </div>
        ) : (
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {roles.map((role) => (
              <Link
                key={role.id}
                href={`/roles/${role.id}`}
                className="group rounded-xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
              >
                <h2 className="text-xl font-semibold text-zinc-900 group-hover:text-blue-600">
                  {role.name}
                </h2>

                <p className="mt-3 text-sm leading-6 text-zinc-600">
                  {role.description || "No description available."}
                </p>

                <div className="mt-5 text-sm font-medium text-blue-600">
                  View role →
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}