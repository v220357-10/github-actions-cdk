from aws_cdk import (
    Stack,
    Aws,
    aws_iam as iam,
)
from constructs import Construct

class GithubOidcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, github_org: str, repo_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        oidc_provider = iam.OpenIdConnectProvider(
            self,
            "GitHubOidcProvider",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
        )
        github_sub_pattern = f"repo:{github_org}/{repo_name}:*"

        github_role = iam.Role(
            self,
            "GitHubActionsDeploymentRole",
            role_name="GitHubActionsDeploymentRole",
            assumed_by=iam.OpenIdConnectPrincipal(oidc_provider).with_conditions(
                {
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                    },
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": github_sub_pattern
                    },
                }
            ),
            description="Role assumed by the GitHub Actions workflows via OIDC for CDK deployment",
        )
        account_id = Aws.ACCOUNT_ID
        region = Aws.REGION

        deploy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "cloudformation:*",
                "s3:*",
                "iam:PassRole",
                "logs:*",
            ],
            resources=["*"],
        )

        qualifier = "hnb659fds"  # default CDK bootstrap qualifier

        ssm_statement = iam.PolicyStatement(
            sid="ReadCdkBootstrapVersion",
            effect=iam.Effect.ALLOW,
            actions=["ssm:GetParameter"],
            resources=[
                f"arn:aws:ssm:{region}:{account_id}:parameter/cdk-bootstrap/{qualifier}/version"
            ],
        )

        bootstrap_role_names = [
            f"cdk-{qualifier}-deploy-role-{account_id}-{region}",
            f"cdk-{qualifier}-file-publishing-role-{account_id}-{region}",
            f"cdk-{qualifier}-image-publishing-role-{account_id}-{region}",
            f"cdk-{qualifier}-lookup-role-{account_id}-{region}",
        ]

        assume_bootstrap_roles = iam.PolicyStatement(
            sid="AssumeCdkBootstrapRoles",
            effect=iam.Effect.ALLOW,
            actions=["sts:AssumeRole"],
            resources=[
                f"arn:aws:iam::{account_id}:role/{role_name}"
                for role_name in bootstrap_role_names
            ],
        )

        policy = iam.Policy(
            self,
            "GitHubActionsPolicy",
            policy_name="GitHubActionsPolicy",
            statements=[
                deploy_statement,
                ssm_statement,
                assume_bootstrap_roles,
            ],
        )

        github_role.attach_inline_policy(policy)