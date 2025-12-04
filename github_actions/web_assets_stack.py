from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    Aspects,
)
from cdk_nag import AwsSolutionsChecks, NagSuppressions

class WebAssetsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, stage_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, f"WebAssetsBucket-{stage_name}",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Apply CDK Nag checks
        Aspects.of(self).add(AwsSolutionsChecks())

        NagSuppressions.add_stack_suppressions(
            self,
            [
                {"id": "AwsSolutions-S1",
                 "reason": "Access logging omitted for brevity in this lab."}
            ],
        )