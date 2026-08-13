import Link from "next/link";
import { searchGraph, type SearchResult } from "../../lib/api";

type Props = {
  searchParams: {
    q?: string;
  };
};

function getResultUrl(result: SearchResult): string | null {
  switch (result.type) {
    case "role":
      return `/roles/${result.id}`;

    case "skill":
      return `/skills/${result.id}`;

    case "ai_opportunity":
      return `/ai-opportunities/${result.id}`;

    case "activity":
      return `/impact/activity/${result.id}`;

    default:
      return null;
  }
}

export default async function SearchPage({ searchParams }: Props) {
  const query = searchParams.q?.trim() ?? "";

  let results: SearchResult[] = [];

  if (query) {
    results = await searchGraph(query);
  }

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">

        <div className="mb-8">
          <Link
            href="/"
            className="text-sm font-medium text-zinc-500 hover:text-zinc-900"
          >
            ← Back to home
          </Link>

          <h1 className="mt-4 text-3xl font-bold text-zinc-900">
            Search Intelligence Graph
          </h1>

          <p className="mt-2 text-zinc-600">
            Search activities, processes, roles, skills, and AI opportunities.
          </p>
        </div>

        <form method="GET" className="mb-8 flex gap-3">
          <input
            name="q"
            defaultValue={query}
            placeholder="Search e.g. assortment, forecasting, merchandising..."
            className="flex-1 rounded-lg border border-zinc-300 bg-white px-4 py-3 outline-none focus:border-zinc-900"
          />

          <button
            type="submit"
            className="rounded-lg bg-zinc-900 px-6 py-3 font-medium text-white hover:bg-zinc-700"
          >
            Search
          </button>
        </form>

        {query && (
          <div className="mb-4 text-sm text-zinc-500">
            {results.length} result{results.length === 1 ? "" : "s"} for{" "}
            <span className="font-semibold text-zinc-900">{`"${query}"`}</span>
          </div>
        )}

        {!query && (
          <div className="rounded-xl border border-dashed border-zinc-300 bg-white p-10 text-center text-zinc-500">
            Enter a search term to explore the intelligence graph.
          </div>
        )}

        {query && results.length === 0 && (
          <div className="rounded-xl border border-zinc-200 bg-white p-10 text-center text-zinc-500">
            No results found.
          </div>
        )}

        <div className="space-y-3">
          {results.map((result) => {
            const url = getResultUrl(result);

            return (
              <div
                key={`${result.type}-${result.id}`}
                className="rounded-xl border border-zinc-200 bg-white p-5 shadow-sm"
              >
                <div className="mb-2 flex items-center gap-3">
                  <span className="rounded-full bg-zinc-100 px-2.5 py-1 text-xs font-semibold uppercase tracking-wide text-zinc-600">
                    {result.type.replace("_", " ")}
                  </span>

                  {url ? (
                    <Link
                      href={url}
                      className="text-lg font-semibold text-zinc-900 hover:underline"
                    >
                      {result.name}
                    </Link>
                  ) : (
                    <span className="text-lg font-semibold text-zinc-900">
                      {result.name}
                    </span>
                  )}
                </div>

                {result.description && (
                  <p className="text-sm leading-6 text-zinc-600">
                    {result.description}
                  </p>
                )}

                {url && (
                  <Link
                    href={url}
                    className="mt-3 inline-block text-sm font-medium text-zinc-900 hover:underline"
                  >
                    View details →
                  </Link>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </main>
  );
}
