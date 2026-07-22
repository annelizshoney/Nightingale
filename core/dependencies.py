from functools import lru_cache

from fastapi import Depends

from app.adk.appointment_agent import AppointmentAgent
from app.adk.client import ADKClient
from app.adk.doctor_agent import DoctorAgent
from app.adk.emergency_agent import EmergencyAgent
from app.adk.family_agent import FamilyAgent
from app.adk.health_agent import HealthAgent
from app.adk.memory_agent import MemoryAgent
from app.adk.medication_agent import MedicationAgent
from app.adk.routine_agent import RoutineAgent
from app.lyzr.agent_registry import AgentRegistry
from app.lyzr.client import LyzrClient
from app.lyzr.orchestrator import LyzrOrchestrator
from app.lyzr.workflow import NightingaleWorkflow
from app.prompts.loader import PromptRepository
from app.qdrant.client import get_qdrant_client
from app.qdrant.config import get_qdrant_config
from app.qdrant.memory_service import MemoryService
from app.repositories.audit_repository import AuditRepository
from app.db.session import get_db
from app.services.audit_service import AuditService
from app.services.appointment_service import AppointmentService
from app.services.doctor_service import DoctorService
from app.services.emergency_service import EmergencyService
from app.services.family_service import FamilyService
from app.services.health_service import HealthService
from app.services.medication_service import MedicationService
from app.services.routine_service import RoutineService


@lru_cache(maxsize=1)
def get_memory_service() -> MemoryService:
    return MemoryService(client=get_qdrant_client(), config=get_qdrant_config())


@lru_cache(maxsize=1)
def get_adk_client() -> ADKClient:
    return ADKClient()


@lru_cache(maxsize=1)
def get_prompt_repository() -> PromptRepository:
    return PromptRepository()


def get_audit_repository(db=Depends(get_db)) -> AuditRepository:
    return AuditRepository(db)


def get_audit_service(db=Depends(get_db)) -> AuditService:
    return AuditService(repository=get_audit_repository(db))


def get_health_agent() -> HealthAgent:
    return HealthAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_medication_agent() -> MedicationAgent:
    return MedicationAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_routine_agent() -> RoutineAgent:
    return RoutineAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_memory_agent() -> MemoryAgent:
    return MemoryAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_appointment_agent() -> AppointmentAgent:
    return AppointmentAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_emergency_agent() -> EmergencyAgent:
    return EmergencyAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_family_agent() -> FamilyAgent:
    return FamilyAgent(client=get_adk_client(), prompts=get_prompt_repository())


def get_doctor_agent() -> DoctorAgent:
    return DoctorAgent(client=get_adk_client(), prompts=get_prompt_repository())


@lru_cache(maxsize=1)
def get_health_service() -> HealthService:
    return HealthService(
        qdrant_client=get_qdrant_client(),
        adk_client=get_adk_client(),
        lyzr_client=get_lyzr_client(),
    )


@lru_cache(maxsize=1)
def get_lyzr_client() -> LyzrClient:
    return LyzrClient()


@lru_cache(maxsize=1)
def get_agent_registry() -> AgentRegistry:
    return AgentRegistry.from_agents(
        memory_agent=get_memory_agent(),
        health_agent=get_health_agent(),
        medication_agent=get_medication_agent(),
        emergency_agent=get_emergency_agent(),
        doctor_agent=get_doctor_agent(),
        family_agent=get_family_agent(),
        appointment_agent=get_appointment_agent(),
        routine_agent=get_routine_agent(),
    )


@lru_cache(maxsize=1)
def get_lyzr_workflow() -> NightingaleWorkflow:
    return NightingaleWorkflow(registry=get_agent_registry())


@lru_cache(maxsize=1)
def get_lyzr_orchestrator() -> LyzrOrchestrator:
    return LyzrOrchestrator(
        registry=get_agent_registry(),
        workflow=get_lyzr_workflow(),
        client=get_lyzr_client(),
        prompts=get_prompt_repository(),
    )


def get_medication_service() -> MedicationService:
    return MedicationService()


def get_routine_service() -> RoutineService:
    return RoutineService()


def get_appointment_service() -> AppointmentService:
    return AppointmentService()


def get_emergency_service() -> EmergencyService:
    return EmergencyService()


def get_family_service() -> FamilyService:
    return FamilyService()


def get_doctor_service() -> DoctorService:
    return DoctorService()
