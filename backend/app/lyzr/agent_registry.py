from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from app.adk.appointment_agent import AppointmentAgent
from app.adk.doctor_agent import DoctorAgent
from app.adk.emergency_agent import EmergencyAgent
from app.adk.family_agent import FamilyAgent
from app.adk.health_agent import HealthAgent
from app.adk.memory_agent import MemoryAgent
from app.adk.medication_agent import MedicationAgent
from app.adk.routine_agent import RoutineAgent


AgentFactory = Callable[[], object]


@dataclass(slots=True)
class AgentRegistry:
    factories: dict[str, AgentFactory] = field(default_factory=dict)
    _cache: dict[str, object] = field(default_factory=dict, init=False, repr=False)

    def get(self, name: str) -> object:
        if name in self._cache:
            return self._cache[name]
        if name not in self.factories:
            raise KeyError(f"Unknown agent: {name}")
        agent = self.factories[name]()
        self._cache[name] = agent
        return agent

    def names(self) -> tuple[str, ...]:
        return tuple(self.factories.keys())

    @classmethod
    def from_agents(
        cls,
        *,
        memory_agent: MemoryAgent,
        health_agent: HealthAgent,
        medication_agent: MedicationAgent,
        emergency_agent: EmergencyAgent,
        doctor_agent: DoctorAgent,
        family_agent: FamilyAgent,
        appointment_agent: AppointmentAgent,
        routine_agent: RoutineAgent,
    ) -> "AgentRegistry":
        return cls(
            factories={
                "memory": lambda: memory_agent,
                "health": lambda: health_agent,
                "medication": lambda: medication_agent,
                "emergency": lambda: emergency_agent,
                "doctor": lambda: doctor_agent,
                "family": lambda: family_agent,
                "appointment": lambda: appointment_agent,
                "routine": lambda: routine_agent,
            }
        )
