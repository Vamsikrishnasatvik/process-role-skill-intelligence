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
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="w-full max-w-xl rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-zinc-900">
          Process × Role × Skill Intelligence Graph
        </h1>

        <p className="mt-3 text-zinc-600">
          Enterprise AI Build Challenge — Phase 0
        </p>

        <div className="mt-8 rounded-xl bg-zinc-50 p-5">
          <p className="text-sm font-medium text-zinc-500">
            Backend Status
          </p>

          <p className="mt-2 text-lg font-semibold">
            {health?.status === "ok" ? "Connected — OK" : "Unavailable"}
          </p>
        </div>
      </div>
    </main>
  );
}