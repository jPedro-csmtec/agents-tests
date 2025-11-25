from fastapi import APIRouter
from services.agent_extraction.app.routers.v1.extraction_info import router as extraction_router
from services.agent_reports.app.routers.v1.reports_info import router as reports_router
from services.agent_cid_analysis.app.routers.v1.analysis_info import router as analysis_router
from services.agent_resume.app.routers.v1.resume_info import router as resumes_router
from services.agent_planner.app.routers.v1.planner_info import router as planners_router
from services.agent_treatment.app.routers.v1.treatment_info import router as treatment_router
from services.agent_diagnostic.app.routers.v1.diagnostic_info import router as diagnostic_router
from services.agent_summary.app.routers.v1.summary_info import router as summary_router
from services.agent_rag.app.routers.v1.rag_info import router as rag_router
from services.agent_analysis_vision.app.routers.v1.vision_info import router as vision_router
from services.agent_allergy.app.routers.v1.allergy_info import router as allergy_router
from services.anamnesis_generator.app.routers.v1.anamnesis_info import router as anamnesis_router
from gateway.app.routers.auth_token import router as router_auth

router = APIRouter()
router.include_router(extraction_router, tags=["extraction-info (v1)"])
router.include_router(reports_router, tags=["reports-info (v1)"])
router.include_router(analysis_router, tags=["analysis-info (v1)"])
router.include_router(resumes_router, tags=["resume-info (v1)"])
router.include_router(planners_router, tags=["planner-info (v1)"])
router.include_router(treatment_router, tags=["treatment-info (v1)"])
router.include_router(diagnostic_router, tags=["diagnostic-info (v1)"])
router.include_router(summary_router, tags=["summary-info (v1)"])
router.include_router(rag_router, tags=["rag-info (v1)"])
router.include_router(vision_router, tags=["vision-info (v1)"])
router.include_router(allergy_router, tags=["allergy-info (v1)"])
router.include_router(anamnesis_router, tags=["anamnesis-info (v1)"])
