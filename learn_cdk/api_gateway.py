from aws_cdk import (
    Duration,
    Stack,
    Aws,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam
)
from constructs import Construct


class MyAPIStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Lambda function for the authorizer
        auth_handler = lambda_.Function(
            self, "AuthHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("learn_cdk/hello_world"),
            handler="hello_world.lambda_handler"
        )

        # Create the authorizer
        authorizer = apigateway.TokenAuthorizer(
            self, "MyAuthorizer",
            handler=auth_handler,
            identity_source=apigateway.IdentitySource.header("Authorization"),
            authorizer_name="MyAuthorizer",
            results_cache_ttl=Duration.seconds(300),
        )

        # Create a Lambda function for the endpoint
        # client_handler = lambda_.Function(
        #     self, "ClientHandler",
        #     runtime=lambda_.Runtime.PYTHON_3_9,
        #     code=lambda_.Code.from_asset("lambda_functions"),
        #     handler="client.handler"
        # )

        # Create the REST API
        api = apigateway.RestApi(
            self, "MyAPI",
            rest_api_name="My API",
            endpoint_types=[apigateway.EndpointType.REGIONAL],
            description="API for my application"
        )

        # Add a resource policy statement to the Lambda function
        auth_handler.add_permission(
            "ApiInvokePermission",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=f"arn:aws:execute-api:{Aws.REGION}:{Aws.ACCOUNT_ID}:{api.rest_api_id}/*/*/*"
        )

        # Create the resource structure
        api_root = api.root.add_resource("api")
        api_v1 = api_root.add_resource("v1")
        api_client = api_v1.add_resource("client")

        # Attach the authorizer to the resource
        api_client.add_method(
            "GET",
            authorizer=authorizer,
            request_parameters={
                "method.request.header.x-authentication-type": True,
                "method.request.header.x-user-id": True
            },
            integration=apigateway.HttpIntegration(
                url="https://example.com/client",
                http_method="GET",
                proxy=True,
                options={
                    "integration_responses": [
                        apigateway.IntegrationResponse(
                            status_code="200",
                        )
                    ],
                    "request_parameters": {
                        "integration.request.header.x-authentication-type": "context.authentication_type",
                        "integration.request.header.x-user-id": "context.user_id"
                    },
                    # "method_responses": [
                    #     apigateway.MethodResponse(
                    #         status_code="200",
                    #         response_parameters={
                    #             "method.response.header.Access-Control-Allow-Origin": True
                    #         }

                    #     ),
                    # ]
                },

            )
        )
