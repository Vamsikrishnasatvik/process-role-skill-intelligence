const API_BASE_URL = "http://localhost:8002";

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