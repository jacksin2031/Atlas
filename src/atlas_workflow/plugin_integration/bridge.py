"""Plugin Runtime bridge for workflow node execution.

Per RFC-0323 (Plugin Integration). Workflow nodes execute through
Plugin Runtime. The runtime MUST NOT invoke plugin implementations
directly.
"""

from __future__ import annotations
from typing import Any

from atlas_workflow.common import PluginError


class PluginBridge:
    """Bridge between Workflow Runtime and Plugin Runtime.

    All node execution goes through this bridge. The workflow runtime
    never calls plugin implementations directly.
    """

    def __init__(
        self,
        plugin_runtime: Any | None = None,
        node_handlers: dict[str, Any] | None = None,
    ) -> None:
        self._plugin_runtime = plugin_runtime
        self._handlers: dict[str, Any] = node_handlers or {}
        self._registered_types: set[str] = set()

    def register_handler(self, node_type: str, handler: Any) -> None:
        """Register a handler for a node type."""
        self._handlers[node_type] = handler
        self._registered_types.add(node_type)

    def unregister_handler(self, node_type: str) -> bool:
        """Unregister a handler for a node type."""
        if node_type in self._handlers:
            del self._handlers[node_type]
            self._registered_types.discard(node_type)
            return True
        return False

    def execute_node(
        self,
        node_type: str,
        node_id: str,
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        node_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a workflow node through the Plugin Runtime.

        Args:
            node_type: The type of node to execute.
            node_id: The unique node identifier.
            configuration: Node configuration parameters.
            inputs: Input data for the node.
            node_metadata: Additional node metadata.

        Returns:
            Output data from node execution.

        Raises:
            PluginError: If the node type is not registered or execution fails.
        """
        if node_type not in self._registered_types:
            raise PluginError(
                f"Node type {node_type!r} is not registered",
                plugin_name=node_type,
            )

        handler = self._handlers.get(node_type)
        if handler is None:
            raise PluginError(
                f"No handler registered for node type {node_type!r}",
                plugin_name=node_type,
            )

        try:
            if callable(handler):
                return handler(
                    node_id=node_id,
                    configuration=configuration,
                    inputs=inputs,
                    metadata=node_metadata,
                )
            else:
                raise PluginError(
                    f"Handler for {node_type!r} is not callable",
                    plugin_name=node_type,
                )
        except PluginError:
            raise
        except Exception as exc:
            raise PluginError(
                f"Node execution failed: {exc}",
                plugin_name=node_type,
                details={"node_id": node_id, "error": str(exc)},
            )

    def get_registered_types(self) -> set[str]:
        """Return the set of registered node types."""
        return set(self._registered_types)

    def has_handler(self, node_type: str) -> bool:
        """Check if a handler is registered for the given node type."""
        return node_type in self._registered_types

    @property
    def plugin_runtime(self) -> Any | None:
        return self._plugin_runtime
