import os
import aws_cdk as cdk
from github_actions.web_assets_stack import WebAssetsStack
from github_actions.github_oidc_stack import GithubOidcStack

app = cdk.App()
account = os.getenv("CDK_DEFAULT_ACCOUNT")
region = os.getenv("CDK_DEFAULT_REGION")

WebAssetsStack(app, "WebAssetsStack-Staging",
               env=cdk.Environment(account=account, region=region),
               stage_name="staging")

WebAssetsStack(app, "WebAssetsStack-Prod",
               env=cdk.Environment(account=account, region=region),
               stage_name="prod")

GithubOidcStack(app, "GithubOidcStack",
                env=cdk.Environment(account=account, region=region),
                github_org="v220357-10", repo_name="github-actions-cdk"
                )
app.synth()