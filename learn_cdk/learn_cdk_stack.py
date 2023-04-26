from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    CfnOutput
)
from constructs import Construct


class LearnCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "LearnCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # Define the Lambda function
        hello_world_lambda = lambda_.Function(
            self,
            "HelloWorldFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("learn_cdk/hello_world"),
            handler="hello_world.lambda_handler",
            memory_size=128,
            timeout=Duration.seconds(10),
        )

        # Add permission for API Gateway to invoke the Lambda function
        # hello_world_lambda.add_permission(
        #     "ApiGatewayInvokePermission",
        #     principal=lambda_.ServicePrincipal("apigateway.amazonaws.com"),
        #     action="lambda:InvokeFunction",
        # )

        api = apigateway.RestApi(
            self, 'HelloWorldAPI',
            rest_api_name='Hello World API',
            description='This is a simple API for the Hello World Lambda function'
        )

        hello_world_resource = api.root.add_resource('hello')
        hello_world_resource.add_method(
            'GET', apigateway.LambdaIntegration(hello_world_lambda))

        # Output the ARN of the Lambda function
        CfnOutput(
            self, "MyLambdaFunctionArn",
            value=hello_world_lambda.function_arn
        )

        # Output the URL of the API Gateway
        CfnOutput(
            self, "HelloWorldAPIUrl",
            value=api.url
        )
