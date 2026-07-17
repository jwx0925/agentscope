# -*- coding: utf-8 -*-
"""Unit tests for OpenSandboxWorkspaceManager."""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from agentscope.app.workspace_manager import OpenSandboxWorkspaceManager


class TestOpenSandboxWorkspaceManagerClosePolicy(IsolatedAsyncioTestCase):
    """Test forwarding of the remote sandbox close policy."""

    @patch(
        "agentscope.app.workspace_manager."
        "_opensandbox_workspace_manager.OpenSandboxWorkspace",
    )
    async def test_kill_on_close_is_forwarded(self, workspace_cls) -> None:
        """Managers can select kill for runtimes without pause support."""
        workspace_cls.return_value.initialize = AsyncMock()
        manager = OpenSandboxWorkspaceManager(kill_on_close=True)

        workspace = (
            await manager._build_and_start(  # pylint: disable=protected-access
                workspace_id="workspace-1",
                user_id="user-1",
                agent_id="agent-1",
            )
        )

        self.assertIs(workspace, workspace_cls.return_value)
        self.assertEqual(workspace_cls.call_args.kwargs["kill_on_close"], True)
        workspace.initialize.assert_awaited_once_with()

    @patch(
        "agentscope.app.workspace_manager."
        "_opensandbox_workspace_manager.OpenSandboxWorkspace",
    )
    async def test_manager_preserves_sandbox_by_default(
        self,
        workspace_cls,
    ) -> None:
        """The cache manager retains its persistence-first default."""
        workspace_cls.return_value.initialize = AsyncMock()
        manager = OpenSandboxWorkspaceManager()

        await manager._build_and_start(  # pylint: disable=protected-access
            workspace_id="workspace-1",
            user_id="user-1",
            agent_id="agent-1",
        )

        self.assertEqual(
            workspace_cls.call_args.kwargs["kill_on_close"], False
        )
