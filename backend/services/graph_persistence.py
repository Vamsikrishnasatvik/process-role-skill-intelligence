from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity
from app.models.process import Process
from app.models.role import Role
from app.models.skill import Skill
from app.schemas.process_analysis import ProcessAnalysisResponse


class GraphPersistenceService:
    """
    Persists an AI-generated process analysis into the
    existing intelligence graph.

    The operation is intentionally transaction-scoped:
    callers should commit only after persistence succeeds.
    """

    def persist_analysis(
        self,
        db: Session,
        process: Process,
        analysis: ProcessAnalysisResponse,
    ) -> list[Activity]:
        persisted_activities: list[Activity] = []

        for generated_activity in analysis.activities:
            activity = self._get_or_create_activity(
                db=db,
                process=process,
                name=generated_activity.name,
                description=generated_activity.description,
            )

            for generated_role in generated_activity.roles:
                role = self._get_or_create_role(
                    db=db,
                    name=generated_role.name,
                    description=generated_role.description,
                )

                if role not in activity.roles:
                    activity.roles.append(role)

                for generated_skill in generated_activity.skills:
                    skill = self._get_or_create_skill(
                        db=db,
                        name=generated_skill.name,
                        description=generated_skill.description,
                    )

                    if skill not in role.skills:
                        role.skills.append(skill)

            for generated_opportunity in generated_activity.ai_opportunities:
                opportunity = self._get_or_create_ai_opportunity(
                    db=db,
                    name=generated_opportunity.name,
                    description=generated_opportunity.description,
                )

                if opportunity not in activity.ai_opportunities:
                    activity.ai_opportunities.append(opportunity)

                # The roles and skills participating in this activity
                # are also impacted by the AI opportunity.
                for role in activity.roles:
                    if role not in opportunity.impacted_roles:
                        opportunity.impacted_roles.append(role)

                    for skill in role.skills:
                        if skill not in opportunity.impacted_skills:
                            opportunity.impacted_skills.append(skill)

            persisted_activities.append(activity)

        return persisted_activities

    def _get_or_create_activity(
        self,
        db: Session,
        process: Process,
        name: str,
        description: str | None,
    ) -> Activity:
        normalized_name = self._normalize(name)

        for activity in process.activities:
            if self._normalize(activity.name) == normalized_name:
                return activity

        activity = Activity(
            process_id=process.id,
            name=name.strip(),
            description=description,
        )

        db.add(activity)
        db.flush()

        return activity

    def _get_or_create_role(
        self,
        db: Session,
        name: str,
        description: str | None,
    ) -> Role:
        normalized_name = self._normalize(name)

        role = (
            db.query(Role)
            .filter(
                func.lower(func.trim(Role.name)) == normalized_name
            )
            .first()
        )

        if role is not None:
            return role

        role = Role(
            name=name.strip(),
            description=description,
        )

        db.add(role)
        db.flush()

        return role

    def _get_or_create_skill(
        self,
        db: Session,
        name: str,
        description: str | None,
    ) -> Skill:
        normalized_name = self._normalize(name)

        skill = (
            db.query(Skill)
            .filter(
                func.lower(func.trim(Skill.name)) == normalized_name
            )
            .first()
        )

        if skill is not None:
            return skill

        skill = Skill(
            name=name.strip(),
            description=description,
        )

        db.add(skill)
        db.flush()

        return skill

    def _get_or_create_ai_opportunity(
        self,
        db: Session,
        name: str,
        description: str | None,
    ) -> AIOpportunity:
        normalized_name = self._normalize(name)

        opportunity = (
            db.query(AIOpportunity)
            .filter(
                func.lower(func.trim(AIOpportunity.name))
                == normalized_name
            )
            .first()
        )

        if opportunity is not None:
            return opportunity

        opportunity = AIOpportunity(
            name=name.strip(),
            description=description,
        )

        db.add(opportunity)
        db.flush()

        return opportunity

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(value.strip().lower().split())


graph_persistence_service = GraphPersistenceService()