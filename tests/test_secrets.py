import boto3
import pytest
from app.secrets import get_secret
from app.settings import Settings
from botocore.exceptions import ClientError
from moto import mock_aws


@pytest.fixture
def settings_(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY", "mocked_access_key")
    monkeypatch.setenv("AWS_SECRET_KEY", "mocked_secret_key")

    return Settings()


@pytest.fixture(scope="function")
def mock_secrets_manager(settings_):
    with mock_aws():
        client = boto3.client(
            "secretsmanager",
            region_name="us-east-1",
            aws_access_key_id=settings_.AWS_ACCESS_KEY,
            aws_secret_access_key=settings_.AWS_SECRET_KEY,
        )

        client.create_secret(Name="my-secret", SecretString="my-secret-value")

        yield client


def test_get_secret_not_found(mock_secrets_manager):
    with pytest.raises(ClientError) as error:
        get_secret("nonexistent-secret")

    assert error.value.response["Error"]["Code"] == "ResourceNotFoundException"
    assert (
        error.value.response["Error"]["Message"]
        == "Secrets Manager can't find the specified secret."
    )
