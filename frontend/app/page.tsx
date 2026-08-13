import Link from "next/link";

async function getBackendHealth() {
  try {
    const response = await fetch("http://backend:8000/health", {
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}

export default async function Home() {
  const health = await getBackendHealth();

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <header className="rounded-3xl bg-zinc-900 p-10 text-white shadow-xl">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-widest text-zinc-400">
              Enterprise AI Intelligence Platform
            </p>

            <h1 className="mt-4 text-4xl font-bold tracking-tight md:text-5xl">
              Process × Role × Skill
              <br />
              Intelligence Graph
            </h1>

            <p className="mt-5 text-lg leading-8 text-zinc-300">
              Analyze enterprise processes, discover the roles and skills
              involved, and identify how AI can transform the work.
            </p>
          </div>
        </header>

        <section className="mt-8 grid gap-5 md:grid-cols-3">
          <Link
            href="/processes"
            className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
          >
            <p className="text-3xl">⚙️</p>

            <h2 className="mt-4 text-xl font-bold text-zinc-900">
              Process Intelligence
            </h2>

            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Analyze business processes and generate activities,
              roles, and skills using AI.
            </p>

            <p className="mt-5 text-sm font-semibold text-zinc-900">
              Explore processes →
            </p>
          </Link>

          <Link
            href="/roles"
            className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
          >
            <p className="text-3xl">👤</p>

            <h2 className="mt-4 text-xl font-bold text-zinc-900">
              Role Intelligence
            </h2>

            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Explore roles, their skills, and the processes they
              participate in.
            </p>

            <p className="mt-5 text-sm font-semibold text-zinc-900">
              Explore roles →
            </p>
          </Link>

          <Link
            href="/ai-opportunities"
            className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
          >
            <p className="text-3xl">✨</p>

            <h2 className="mt-4 text-xl font-bold text-zinc-900">
              AI Opportunities
            </h2>

            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Discover AI opportunities and understand their impact
              on roles and skills.
            </p>

            <p className="mt-5 text-sm font-semibold text-zinc-900">
              Explore opportunities →
            </p>
          </Link>
        </section>

        <section className="mt-8 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-400">
                System Status
              </p>

              <p className="mt-2 text-lg font-semibold text-zinc-900">
                Backend{" "}
                {health?.status === "ok"
                  ? "Connected"
                  : "Unavailable"}
              </p>
            </div>

            <div
              className={`h-3 w-3 rounded-full ${
                health?.status === "ok"
                  ? "bg-green-500"
                  : "bg-red-500"
              }`}
            />
          </div>
        </section>
      </div>
    </main>
  );
}