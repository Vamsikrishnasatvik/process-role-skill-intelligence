from fastapi import FastAPI

from app.api.activities import router as activities_router
from app.api.industries import router as industries_router
from app.api.processes import router as processes_router
from app.api.value_chain_stages import router as stages_router
from app.api.roles import router as roles_router
from app.api.skills import router as skills_router
from app.api.activity_roles import router as activity_roles_router
from app.api.role_skills import router as role_skills_router
from app.api.ai_opportunities import router as ai_opportunities_router
from app.api.activity_ai_opportunities import router as activity_ai_opportunities_router
from app.api.ai_opportunity_roles import router as ai_opportunity_roles_router
from app.api.ai_opportunity_skills import router as ai_opportunity_skills_router
from app.api.graph import router as graph_router


app = FastAPI(
    title="Process × Role × Skill Intelligence Graph API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(industries_router)
app.include_router(stages_router)
app.include_router(processes_router)
app.include_router(activities_router)
app.include_router(roles_router)
app.include_router(skills_router)
app.include_router(activity_roles_router)
app.include_router(role_skills_router)
app.include_router(ai_opportunities_router)
app.include_router(activity_ai_opportunities_router)
app.include_router(ai_opportunity_roles_router)
app.include_router(ai_opportunity_skills_router)
app.include_router(graph_router)