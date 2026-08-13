from app.schemas.process_analysis import (
    GeneratedActivity,
    GeneratedAIOpportunity,
    GeneratedRole,
    GeneratedSkill,
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)

from services.providers.base import AIProvider


class MockProvider(AIProvider):
    """
    Deterministic enterprise process-analysis provider.

    Used for local development, testing, and demos.
    No external AI API calls are made.
    """

    def analyze_process(
        self,
        process_name: str,
        process_description: str | None,
        payload: ProcessAnalysisRequest,
    ) -> ProcessAnalysisResponse:

        normalized = process_name.strip().lower()

        if "assortment" in normalized:
            activities = self._assortment_planning()

        elif "inventory" in normalized or "replenishment" in normalized:
            activities = self._inventory_replenishment()

        elif "schedule" in normalized:
            activities = self._store_scheduling()

        else:
            activities = self._generic_process(process_name)

        return ProcessAnalysisResponse(
            process_name=process_name,
            process_description=process_description,
            activities=activities,
        )

    def _assortment_planning(self) -> list[GeneratedActivity]:
        return [
            GeneratedActivity(
                name="Analyze Category Performance",
                description=(
                    "Evaluate historical sales, category performance, "
                    "customer demand, and channel-level trends."
                ),
                roles=[
                    GeneratedRole(
                        name="Merchandising Analyst",
                        description=(
                            "Analyzes category and product performance "
                            "to support assortment decisions."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Category Analytics",
                        description=(
                            "Ability to evaluate category performance "
                            "using sales and demand data."
                        ),
                    ),
                    GeneratedSkill(
                        name="Data Analysis",
                        description=(
                            "Ability to identify trends, patterns, "
                            "and performance drivers in business data."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI-Assisted Category Analytics",
                        description=(
                            "Use AI to identify category trends, anomalies, "
                            "and emerging product demand patterns."
                        ),
                    ),
                ],
            ),
            GeneratedActivity(
                name="Define Product Assortment",
                description=(
                    "Determine which products should be offered across "
                    "stores and retail channels."
                ),
                roles=[
                    GeneratedRole(
                        name="Category Manager",
                        description=(
                            "Owns assortment decisions and balances "
                            "customer demand with commercial objectives."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Assortment Strategy",
                        description=(
                            "Ability to design product assortments "
                            "based on customer and business requirements."
                        ),
                    ),
                    GeneratedSkill(
                        name="Commercial Decision Making",
                        description=(
                            "Ability to evaluate commercial trade-offs "
                            "and select appropriate products."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI-Assisted Assortment Optimization",
                        description=(
                            "Use AI to recommend optimal product assortments "
                            "based on demand, sales, and channel constraints."
                        ),
                    ),
                ],
            ),
            GeneratedActivity(
                name="Evaluate Product Demand",
                description=(
                    "Estimate expected demand for products across "
                    "retail channels and planning periods."
                ),
                roles=[
                    GeneratedRole(
                        name="Demand Planner",
                        description=(
                            "Forecasts product demand and supports "
                            "inventory and assortment planning."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Demand Forecasting",
                        description=(
                            "Ability to estimate future product demand "
                            "using historical and market signals."
                        ),
                    ),
                    GeneratedSkill(
                        name="Forecast Interpretation",
                        description=(
                            "Ability to interpret forecasts and translate "
                            "them into planning decisions."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI Demand Forecasting",
                        description=(
                            "Generate demand forecasts using historical "
                            "sales patterns and relevant business signals."
                        ),
                    ),
                ],
            ),
            GeneratedActivity(
                name="Approve Assortment",
                description=(
                    "Review proposed assortments and approve the final "
                    "product selection for each retail channel."
                ),
                roles=[
                    GeneratedRole(
                        name="Merchandising Manager",
                        description=(
                            "Reviews assortment recommendations and "
                            "approves commercial decisions."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Merchandising Strategy",
                        description=(
                            "Ability to align product selection with "
                            "commercial and customer objectives."
                        ),
                    ),
                    GeneratedSkill(
                        name="Decision Making",
                        description=(
                            "Ability to evaluate recommendations and "
                            "make accountable business decisions."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI-Assisted Assortment Recommendation",
                        description=(
                            "Provide ranked assortment recommendations "
                            "while keeping final approval with business users."
                        ),
                    ),
                ],
            ),
        ]

    def _inventory_replenishment(self) -> list[GeneratedActivity]:
        return [
            GeneratedActivity(
                name="Monitor Inventory Levels",
                description=(
                    "Monitor inventory positions across stores and "
                    "distribution channels."
                ),
                roles=[
                    GeneratedRole(
                        name="Inventory Analyst",
                        description=(
                            "Monitors inventory availability and identifies "
                            "potential stock issues."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Inventory Analysis",
                        description=(
                            "Ability to analyze inventory positions "
                            "and identify exceptions."
                        ),
                    ),
                    GeneratedSkill(
                        name="Data Analysis",
                        description=(
                            "Ability to interpret operational data "
                            "and identify meaningful patterns."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI Inventory Monitoring",
                        description=(
                            "Automatically identify inventory anomalies "
                            "and potential stock-out risks."
                        ),
                    ),
                ],
            ),
            GeneratedActivity(
                name="Forecast Replenishment Demand",
                description=(
                    "Estimate future inventory requirements using "
                    "demand and inventory signals."
                ),
                roles=[
                    GeneratedRole(
                        name="Demand Planner",
                        description=(
                            "Forecasts demand and determines future "
                            "inventory requirements."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Demand Forecasting",
                        description=(
                            "Ability to estimate future demand "
                            "using historical business data."
                        ),
                    ),
                    GeneratedSkill(
                        name="Inventory Planning",
                        description=(
                            "Ability to translate demand forecasts "
                            "into inventory requirements."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI Replenishment Forecasting",
                        description=(
                            "Predict replenishment requirements and "
                            "identify upcoming inventory risks."
                        ),
                    ),
                ],
            ),
            GeneratedActivity(
                name="Create Replenishment Recommendations",
                description=(
                    "Determine when and how much inventory should "
                    "be replenished."
                ),
                roles=[
                    GeneratedRole(
                        name="Replenishment Planner",
                        description=(
                            "Creates replenishment recommendations "
                            "based on inventory and demand."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Replenishment Planning",
                        description=(
                            "Ability to determine replenishment "
                            "quantities and timing."
                        ),
                    ),
                    GeneratedSkill(
                        name="Supply Planning",
                        description=(
                            "Ability to balance inventory requirements "
                            "with supply constraints."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI Replenishment Optimization",
                        description=(
                            "Recommend replenishment quantities and timing "
                            "based on demand and inventory conditions."
                        ),
                    ),
                ],
            ),
        ]

    def _store_scheduling(self) -> list[GeneratedActivity]:
        return [
            GeneratedActivity(
                name="Forecast Staffing Requirements",
                description=(
                    "Estimate staffing requirements using store demand "
                    "and operational workload."
                ),
                roles=[
                    GeneratedRole(
                        name="Store Operations Planner",
                        description=(
                            "Plans staffing requirements based on "
                            "store operations and expected demand."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Workforce Planning",
                        description=(
                            "Ability to determine workforce requirements "
                            "based on operational demand."
                        ),
                    ),
                    GeneratedSkill(
                        name="Demand Analysis",
                        description=(
                            "Ability to interpret demand patterns "
                            "and staffing implications."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI Staffing Forecasting",
                        description=(
                            "Predict staffing requirements based on "
                            "historical demand and operational patterns."
                        ),
                    ),
                ],
            ),
            GeneratedActivity(
                name="Create Employee Schedule",
                description=(
                    "Create employee schedules that balance staffing "
                    "requirements, availability, and operational constraints."
                ),
                roles=[
                    GeneratedRole(
                        name="Store Manager",
                        description=(
                            "Creates and reviews employee schedules "
                            "for store operations."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Workforce Scheduling",
                        description=(
                            "Ability to create schedules while "
                            "balancing staffing constraints."
                        ),
                    ),
                    GeneratedSkill(
                        name="Resource Allocation",
                        description=(
                            "Ability to allocate available employees "
                            "to operational requirements."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI-Assisted Workforce Scheduling",
                        description=(
                            "Generate optimized schedules based on demand, "
                            "availability, and staffing constraints."
                        ),
                    ),
                ],
            ),
        ]

    def _generic_process(
        self,
        process_name: str,
    ) -> list[GeneratedActivity]:
        return [
            GeneratedActivity(
                name=f"Analyze {process_name}",
                description=(
                    f"Analyze the activities and operational requirements "
                    f"involved in {process_name.lower()}."
                ),
                roles=[
                    GeneratedRole(
                        name="Process Analyst",
                        description=(
                            "Analyzes process performance and supports "
                            "business improvement decisions."
                        ),
                    ),
                ],
                skills=[
                    GeneratedSkill(
                        name="Process Analysis",
                        description=(
                            "Ability to analyze business processes, "
                            "identify patterns, and support improvements."
                        ),
                    ),
                ],
                ai_opportunities=[
                    GeneratedAIOpportunity(
                        name="AI-Assisted Process Optimization",
                        description=(
                            "Use AI to identify process improvement "
                            "opportunities and support decision-making."
                        ),
                    ),
                ],
            )
        ]