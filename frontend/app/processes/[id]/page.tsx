import Link from "next/link";
import { getActivities, getProcess } from "../../../lib/api";
import AnalyzeProcess from "./AnalyzeProcess";

type PageProps = {
  params: {
    id: string;
  };
};

export default async function ProcessPage({
  params,
}: PageProps) {
  const [process, allActivities] = await Promise.all([
    getProcess(params.id),
    getActivities(),
  ]);

  const activities = allActivities.filter(
    (activity) => activity.process_id === process.id
  );

  return (
    <main className="min-h-screen bg-zinc-50 p-8">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/processes"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Back to Processes
        </Link>

        <div className="mt-6 rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-start">
            <div>
              <div className="inline-flex rounded-lg bg-zinc-100 px-3 py-1 text-xs font-semibold text-zinc-600">
                BUSINESS PROCESS
              </div>

              <h1 className="mt-4 text-3xl font-bold text-zinc-900">
                {process.name}
              </h1>

              <p className="mt-3 max-w-3xl leading-7 text-zinc-600">
                {process.description || "No description available."}
              </p>
            </div>

            <AnalyzeProcess
              processId={process.id}
              name={process.name}
              description={process.description}
            />
          </div>
        </div>

        <section className="mt-8">
          <div className="mb-4">
            <h2 className="text-xl font-bold text-zinc-900">
              Process Activities
            </h2>

            <p className="mt-1 text-sm text-zinc-500">
              Activities currently represented in the intelligence graph.
            </p>
          </div>

          {activities.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-zinc-300 bg-white p-10 text-center">
              <p className="text-zinc-500">
                No activities have been generated for this process yet.
              </p>

              <p className="mt-2 text-sm text-zinc-400">
                Use &quot;Analyze with AI&quot; to generate process intelligence.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {activities.map((activity) => (
                <div
                  key={activity.id}
                  className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm"
                >
                  <h3 className="text-lg font-semibold text-zinc-900">
                    {activity.name}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-zinc-600">
                    {activity.description ||
                      "No activity description available."}
                  </p>

                  <div className="mt-5">
                    <Link
                      href={`/impact/activity/${activity.id}`}
                      className="text-sm font-medium text-zinc-900 hover:underline"
                    >
                      Explore activity impact →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}