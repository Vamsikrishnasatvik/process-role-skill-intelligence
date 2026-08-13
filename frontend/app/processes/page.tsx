import Link from "next/link";
import { getProcesses } from "../../lib/api";

export default async function ProcessesPage() {
  const processes = await getProcesses();

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8">
          <Link
            href="/"
            className="text-sm text-zinc-500 hover:text-zinc-900"
          >
            ← Dashboard
          </Link>

          <h1 className="mt-4 text-3xl font-bold text-zinc-900">
            Business Processes
          </h1>

          <p className="mt-2 text-zinc-600">
            Explore enterprise processes and analyze their activities,
            roles, and required skills.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {processes.map((process) => (
            <Link
              key={process.id}
              href={`/processes/${process.id}`}
              className="group rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:border-zinc-400 hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <div className="rounded-lg bg-zinc-100 px-3 py-1 text-xs font-semibold text-zinc-600">
                  PROCESS
                </div>

                <span className="text-zinc-400 transition group-hover:translate-x-1">
                  →
                </span>
              </div>

              <h2 className="mt-5 text-xl font-semibold text-zinc-900">
                {process.name}
              </h2>

              <p className="mt-3 line-clamp-3 text-sm leading-6 text-zinc-600">
                {process.description || "No description available."}
              </p>

              <div className="mt-6 text-sm font-medium text-zinc-900">
                View process intelligence →
              </div>
            </Link>
          ))}
        </div>

        {processes.length === 0 && (
          <div className="rounded-2xl border border-dashed border-zinc-300 bg-white p-12 text-center">
            <h2 className="text-lg font-semibold text-zinc-900">
              No processes found
            </h2>

            <p className="mt-2 text-sm text-zinc-500">
              Create a process in the backend before analyzing it.
            </p>
          </div>
        )}
      </div>
    </main>
  );
}