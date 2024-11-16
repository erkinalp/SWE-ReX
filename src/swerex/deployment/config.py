from pathlib import PurePath
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from swerex.deployment.abstract import AbstractDeployment


class ModalDeploymentConfig(BaseModel):
    image: str | PurePath
    """Image to use for the deployment.
    """
    startup_timeout: float = 0.4
    """The time to wait for the runtime to start."""
    runtime_timeout: float = 1800.0
    """The runtime timeout."""
    modal_sandbox_kwargs: dict[str, Any] = {}
    """Additional arguments to pass to `modal.Sandbox.create`"""

    type: Literal["modal"] = "modal"
    """Discriminator for (de)serialization/CLI. Do not change."""

    model_config = ConfigDict(extra="forbid")

    def get_deployment(self) -> AbstractDeployment:
        from swerex.deployment.modal import ModalDeployment

        return ModalDeployment.from_config(self)


class DockerDeploymentConfig(BaseModel):
    image: str
    """The name of the docker image to use."""
    port: int | None = None
    """The port that the docker container connects to. If None, a free port is found."""
    docker_args: list[str] = []
    """Additional arguments to pass to the docker run command."""
    startup_timeout: float = 60.0
    """The time to wait for the runtime to start."""
    pull: Literal["never", "always", "missing"] = "missing"
    """When to pull docker images."""
    remove_images: bool = False
    """Whether to remove the image after it has stopped."""

    type: Literal["docker"] = "docker"
    """Discriminator for (de)serialization/CLI. Do not change."""

    model_config = ConfigDict(extra="forbid")

    def get_deployment(self) -> AbstractDeployment:
        from swerex.deployment.docker import DockerDeployment

        return DockerDeployment.from_config(self)


class DummyDeploymentConfig(BaseModel):
    type: Literal["dummy"] = "dummy"
    """Discriminator for (de)serialization/CLI. Do not change."""

    model_config = ConfigDict(extra="forbid")

    def get_deployment(self) -> AbstractDeployment:
        from swerex.deployment.dummy import DummyDeployment

        return DummyDeployment.from_config(self)


class FargateDeploymentConfig(BaseModel):
    image: str
    port: int = 8880
    cluster_name: str = "swe-rex-cluster"
    execution_role_prefix: str = "swe-rex-execution-role"
    task_definition_prefix: str = "swe-rex-task"
    log_group: str | None = "/ecs/swe-rex-deployment"
    security_group_prefix: str = "swe-rex-deployment-sg"
    fargate_args: dict[str, str] = {}
    container_timeout: float = 60 * 15
    runtime_timeout: float = 30

    type: Literal["fargate"] = "fargate"
    """Discriminator for (de)serialization/CLI. Do not change."""

    model_config = ConfigDict(extra="forbid")

    def get_deployment(self) -> AbstractDeployment:
        from swerex.deployment.fargate import FargateDeployment

        return FargateDeployment.from_config(self)


class LocalDeploymentConfig(BaseModel):
    """The port that the runtime connects to."""

    type: Literal["local"] = "local"
    """Discriminator for (de)serialization/CLI. Do not change."""

    model_config = ConfigDict(extra="forbid")

    def get_deployment(self) -> AbstractDeployment:
        from swerex.deployment.local import LocalDeployment

        return LocalDeployment.from_config(self)


class RemoteDeploymentConfig(BaseModel):
    auth_token: str
    """The token to use for authentication."""
    host: str = "http://127.0.0.1"
    """The host to connect to."""
    port: int | None = None
    """The port to connect to."""
    timeout: float = 0.15

    type: Literal["remote"] = "remote"
    """Discriminator for (de)serialization/CLI. Do not change."""

    model_config = ConfigDict(extra="forbid")

    def get_deployment(self) -> AbstractDeployment:
        from swerex.deployment.remote import RemoteDeployment

        return RemoteDeployment.from_config(self)


DeploymentConfig = (
    LocalDeploymentConfig
    | DockerDeploymentConfig
    | ModalDeploymentConfig
    | FargateDeploymentConfig
    | RemoteDeploymentConfig
)


def get_deployment(
    config: DeploymentConfig,
) -> AbstractDeployment:
    return config.get_deployment()
