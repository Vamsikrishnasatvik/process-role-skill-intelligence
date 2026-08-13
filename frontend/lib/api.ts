const API_BASE_URL =
  process.env.API_BASE_URL || "http://localhost:8002";

async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

/* =========================================================
   Types
   ========================================================= */

export type Role = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type Skill = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type Process = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type AIOpportunity = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

/* =========================================================
   Activity Impact Types
   ========================================================= */

export type ImpactActivity = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type ImpactProcess = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type ImpactOpportunity = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type ImpactRole = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type ImpactSkill = {
  id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type ActivityImpact = {
  activity: ImpactActivity;
  process: ImpactProcess;
  ai_opportunities: ImpactOpportunity[];
  impacted_roles: ImpactRole[];
  impacted_skills: ImpactSkill[];

  impact: {
    type: string;
    automation_levels: string[];
    ai_patterns: string[];
    role_change: string;
    skill_change: string;
    future_change: string;
  };
};

export type Activity = {
  id: string;
  process_id: string;
  name: string;
  description: string | null;
  metadata: Record<string, unknown>;
};

export type GeneratedRole = {
  name: string;
  description: string | null;
};

export type GeneratedSkill = {
  name: string;
  description: string | null;
};

export type GeneratedAIOpportunity = {
  name: string;
  description: string | null;
};

export type GeneratedActivity = {
  name: string;
  description: string | null;
  roles: GeneratedRole[];
  skills: GeneratedSkill[];
  ai_opportunities: GeneratedAIOpportunity[];
};

export type ProcessAnalysis = {
  process_name: string;
  process_description: string | null;
  activities: GeneratedActivity[];
};

/* =========================================================
   Roles
   ========================================================= */

export async function getRoles(): Promise<Role[]> {
  return apiFetch<Role[]>("/api/roles");
}

export async function getRole(id: string): Promise<Role> {
  return apiFetch<Role>(`/api/roles/${id}`);
}

export async function getRoleSkills(id: string): Promise<Skill[]> {
  return apiFetch<Skill[]>(`/api/roles/${id}/skills`);
}

export async function getRoleProcesses(id: string): Promise<Process[]> {
  return apiFetch<Process[]>(`/api/roles/${id}/processes`);
}

/* =========================================================
   Skills
   ========================================================= */

export async function getSkills(): Promise<Skill[]> {
  return apiFetch<Skill[]>("/api/skills");
}

export async function getSkill(id: string): Promise<Skill> {
  return apiFetch<Skill>(`/api/skills/${id}`);
}

export async function getSkillRoles(id: string): Promise<Role[]> {
  return apiFetch<Role[]>(`/api/skills/${id}/roles`);
}

export async function getSkillProcesses(id: string): Promise<Process[]> {
  return apiFetch<Process[]>(`/api/skills/${id}/processes`);
}

/* =========================================================
   AI Opportunities
   ========================================================= */

export async function getAIOpportunities(): Promise<AIOpportunity[]> {
  return apiFetch<AIOpportunity[]>("/api/ai-opportunities");
}

export async function getAIOpportunity(
  id: string
): Promise<AIOpportunity> {
  return apiFetch<AIOpportunity>(
    `/api/ai-opportunities/${id}`
  );
}

/* =========================================================
   Activity → AI Opportunities
   ========================================================= */

export async function getActivityAIOpportunities(
  id: string
): Promise<AIOpportunity[]> {
  return apiFetch<AIOpportunity[]>(
    `/api/activities/${id}/ai-opportunities`
  );
}

/* =========================================================
   AI Opportunity → Roles
   ========================================================= */

export async function getAIOpportunityRoles(
  id: string
): Promise<Role[]> {
  return apiFetch<Role[]>(
    `/api/ai-opportunities/${id}/roles`
  );
}

/* =========================================================
   AI Opportunity → Skills
   ========================================================= */

export async function getAIOpportunitySkills(
  id: string
): Promise<Skill[]> {
  return apiFetch<Skill[]>(
    `/api/ai-opportunities/${id}/skills`
  );
}

/* =========================================================
   Activity → Impact Explorer
   ========================================================= */

export async function getActivityImpact(
  id: string
): Promise<ActivityImpact> {
  return apiFetch<ActivityImpact>(
    `/api/impact/activity/${id}`
  );
}

/* =========================================================
   Evidence
   ========================================================= */

export type Evidence = {
  id: string;
  entity_type: string;
  entity_id: string;
  source_title: string;
  source_type: string;
  snippet: string | null;
  source_url: string | null;
  retrieved_at: string;
  metadata: Record<string, unknown>;
};

export async function getEvidence(
  entityType: string,
  entityId: string
): Promise<Evidence[]> {
  return apiFetch<Evidence[]>(
    `/api/evidence/${entityType}/${entityId}`
  );
}

/* =========================================================
   Global Search
   ========================================================= */

export type SearchResult = {
  id: string;
  type: "activity" | "process" | "role" | "skill" | "ai_opportunity";
  name: string;
  description: string | null;
};

export async function searchGraph(
  query: string
): Promise<SearchResult[]> {
  return apiFetch<SearchResult[]>(
    `/api/search?q=${encodeURIComponent(query)}`
  );
}

/* =========================================================
   Processes
   ========================================================= */

export async function getProcesses(): Promise<Process[]> {
  return apiFetch<Process[]>("/api/processes");
}

export async function getProcess(id: string): Promise<Process> {
  return apiFetch<Process>(`/api/processes/${id}`);
}

/* =========================================================
   Activities
   ========================================================= */

export async function getActivities(): Promise<Activity[]> {
  return apiFetch<Activity[]>("/api/activities");
}

/* =========================================================
   Process AI Analysis
   ========================================================= */

export async function analyzeProcess(
  id: string,
  payload: {
    name: string;
    description?: string | null;
  }
): Promise<ProcessAnalysis> {
  const response = await fetch(
    `${API_BASE_URL}/api/processes/${id}/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(`AI analysis failed: ${response.status}`);
  }

  return response.json();
}