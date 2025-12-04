import aws_cdk as core
import aws_cdk.assertions as assertions

from github_actions.github_actions_stack import GithubActionsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in github_actions/github_actions_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GithubActionsStack(app, "github-actions")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
