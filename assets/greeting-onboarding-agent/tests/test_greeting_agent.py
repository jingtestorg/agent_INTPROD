"""Unit and integration tests for the Greeting Onboarding Agent."""

from __future__ import annotations

import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_llm_response(content: str):
    """Create a mock LLM message object."""
    msg = MagicMock()
    msg.content = content
    return msg


def _make_agent_result(response_text: str) -> dict:
    return {"messages": [_make_llm_response(response_text)]}


# ---------------------------------------------------------------------------
# Unit Tests
# ---------------------------------------------------------------------------


class TestGreeting:
    """R1 — Personalised Greeting: agent introduces itself and asks for name."""

    @pytest.mark.asyncio
    async def test_agent_greets_and_asks_for_name(self, add_agent_to_path):
        """Agent should introduce itself and ask for the employee's name."""
        from agent import SampleAgent

        greeting_response = (
            "Hello! I'm Onboard, your onboarding assistant. Welcome to the company! "
            "To get started, could you please tell me your name?"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(greeting_response)
            result = await agent.invoke("Hi", "ctx-test-greeting", tools=[])

        assert result.status == "completed"
        assert any(kw in result.message.lower() for kw in ["name", "hello", "welcome"]), (
            f"Expected greeting with name prompt, got: {result.message}"
        )

    @pytest.mark.asyncio
    async def test_agent_uses_name_after_introduction(self, add_agent_to_path):
        """Agent should address the employee by name once provided."""
        from agent import SampleAgent

        response_with_name = (
            "Nice to meet you, Alex! Great to have you on board. "
            "Could you also tell me your role or department?"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(response_with_name)
            result = await agent.invoke("My name is Alex", "ctx-test-name", tools=[])

        assert result.status == "completed"
        assert "alex" in result.message.lower(), (
            f"Expected agent to use employee name 'Alex', got: {result.message}"
        )


class TestRoleCollection:
    """R2 — Role Collection: agent asks for role after collecting name."""

    @pytest.mark.asyncio
    async def test_agent_asks_for_role(self, add_agent_to_path):
        """Agent should ask for the employee's role after receiving their name."""
        from agent import SampleAgent

        response = (
            "Nice to meet you, Alex! Great to have you. "
            "What is your role or department?"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(response)
            result = await agent.invoke("I am Alex", "ctx-test-role", tools=[])

        assert result.status == "completed"
        assert any(kw in result.message.lower() for kw in ["role", "department", "position"]), (
            f"Expected agent to ask for role, got: {result.message}"
        )


class TestOnboardingWalkthrough:
    """R3 — Step-by-Step Onboarding Guidance."""

    @pytest.mark.asyncio
    async def test_agent_presents_first_step(self, add_agent_to_path):
        """Agent should start with Step 1 when walkthrough begins."""
        from agent import SampleAgent

        step1_response = (
            "Great! Let's begin your onboarding. Step 1: IT Setup. "
            "Please log in to your company laptop and connect to VPN. "
            "Let me know when you've completed these steps!"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(step1_response)
            result = await agent.invoke(
                "I am Alex, my role is Software Engineer", "ctx-test-walkthrough", tools=[]
            )

        assert result.status == "completed"
        assert any(kw in result.message.lower() for kw in ["step 1", "it setup", "laptop", "vpn"]), (
            f"Expected Step 1 content, got: {result.message}"
        )

    @pytest.mark.asyncio
    async def test_agent_moves_to_next_step_on_acknowledgement(self, add_agent_to_path):
        """Agent should progress to Step 2 after employee acknowledges Step 1."""
        from agent import SampleAgent

        step2_response = (
            "Excellent! Step 2: System Access. "
            "Check your inbox for tool invitations and accept them. "
            "Ready to move on?"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(step2_response)
            result = await agent.invoke("Done, ready for next step", "ctx-test-next", tools=[])

        assert result.status == "completed"
        assert any(kw in result.message.lower() for kw in ["step 2", "system access", "invitation"]), (
            f"Expected Step 2 content, got: {result.message}"
        )


class TestCompletionConfirmation:
    """R4 — Completion Confirmation."""

    @pytest.mark.asyncio
    async def test_agent_delivers_completion_message(self, add_agent_to_path):
        """Agent should deliver an unambiguous completion message after all steps."""
        from agent import SampleAgent

        completion_response = (
            "That's everything, Alex! You've completed your onboarding. "
            "Welcome to the team — you're all set to start. "
            "If you ever have questions, feel free to ask. Good luck on your first day!"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(completion_response)
            result = await agent.invoke("Done with all steps", "ctx-test-complete", tools=[])

        assert result.status == "completed"
        assert any(kw in result.message.lower() for kw in [
            "completed your onboarding", "you're all set", "welcome to the team"
        ]), f"Expected completion message, got: {result.message}"


class TestOffTopicHandling:
    """R5 — Graceful Handling of Off-Topic Input."""

    @pytest.mark.asyncio
    async def test_agent_handles_off_topic_gracefully(self, add_agent_to_path):
        """Agent should acknowledge off-topic input and redirect to onboarding."""
        from agent import SampleAgent

        off_topic_response = (
            "That's a great question! Unfortunately I'm not able to help with weather updates, "
            "but let's make sure you finish your onboarding first. "
            "Where were we — Step 2: System Access. Ready to continue?"
        )

        agent = SampleAgent()
        with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = _make_agent_result(off_topic_response)
            result = await agent.invoke("What is the weather today?", "ctx-test-offtopic", tools=[])

        assert result.status == "completed"
        # Should not abandon onboarding
        assert any(kw in result.message.lower() for kw in ["onboarding", "step", "continue", "where were we"]), (
            f"Expected redirect to onboarding, got: {result.message}"
        )
        # Should acknowledge the off-topic question politely
        assert any(kw in result.message.lower() for kw in [
            "not able to help", "unfortunately", "great question", "can't help with that"
        ]), f"Expected polite acknowledgement, got: {result.message}"


# ---------------------------------------------------------------------------
# Integration Test
# ---------------------------------------------------------------------------


class TestEndToEndOnboarding:
    """Integration test: full onboarding flow from greeting to completion."""

    @pytest.mark.asyncio
    async def test_full_onboarding_flow(self, add_agent_to_path):
        """End-to-end flow: greeting → name → role → steps → completion."""
        from agent import SampleAgent

        conversation_flow = [
            # Turn 1: greeting
            "Hello! I'm Onboard, your onboarding assistant. What is your name?",
            # Turn 2: name collected, ask for role
            "Nice to meet you, Jordan! Great to have you on board. What is your role?",
            # Turn 3: role collected, start walkthrough
            "Wonderful! Let's begin. Step 1: IT Setup — log in to your laptop and connect to VPN.",
            # Turn 4: step 1 done, present step 2
            "Great work! Step 2: System Access — check your inbox for tool invitations.",
            # Turn 5: step 2 done, present step 3
            "Step 3: Team Introduction — introduce yourself in the team channel.",
            # Turn 6: step 3 done, present step 4
            "Step 4: Policies Overview — review the Code of Conduct and other policies.",
            # Turn 7: step 4 done, present step 5
            "Last step! Step 5: Day-One Checklist — verify everything is in order.",
            # Turn 8: completion
            "That's everything, Jordan! You've completed your onboarding. Welcome to the team — you're all set to start.",
        ]

        user_inputs = [
            "Hi there",
            "My name is Jordan",
            "I am a Product Manager",
            "Done with IT setup",
            "Got system access",
            "Introduced myself",
            "Reviewed policies",
            "All done",
        ]

        agent = SampleAgent()
        responses = []

        for i, (user_input, agent_response) in enumerate(zip(user_inputs, conversation_flow)):
            with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
                mock_invoke.return_value = _make_agent_result(agent_response)
                result = await agent.invoke(user_input, f"ctx-integration-{i}", tools=[])
                responses.append(result.message)
                assert result.status == "completed", f"Turn {i+1} did not complete: {result}"

        # Validate key checkpoints
        assert any("name" in r.lower() or "hello" in r.lower() for r in responses[:2]), \
            "Greeting turn should ask for name"
        assert any("role" in r.lower() or "department" in r.lower() for r in responses[:3]), \
            "Should ask for role after name"
        assert any("step" in r.lower() for r in responses[2:-1]), \
            "Walkthrough turns should reference steps"
        assert any(kw in responses[-1].lower() for kw in [
            "completed your onboarding", "all set to start", "welcome to the team"
        ]), f"Final turn should be completion message, got: {responses[-1]}"
