import aws_cdk as core
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_iam as iam
from constructs import Construct


class TodoListApiStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")]
        )

        crud_polycy = iam.PolicyStatement(
            actions=[
                "dynamodb:Scan",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem"
            ],
            resources=["*"]
        )

        clean_db_polycy = iam.PolicyStatement(
            actions=[
                "dynamodb:Scan",
                "dynamodb:DeleteItem"
            ],
            resources=["*"]
        )

        table = dynamodb.Table(self, "TodoListTable",
                                partition_key=dynamodb.Attribute(
                                name="id", type=dynamodb.AttributeType.STRING),
                                removal_policy=core.RemovalPolicy.DESTROY)
        

        todo_function = _lambda.Function(self, "TodoFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler="handler.lambda_handler",
                                         code=_lambda.Code.from_asset("api/"),
                                         environment={
                                             "TABLE_NAME": table.table_name
                                         })
        todo_function.role.attach_inline_policy(iam.Policy(self, "CRUDPolycy", statements=[crud_polycy]))
        table.grant_read_write_data(todo_function)


        clean_db_function = _lambda.Function(self, "CleanDBFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler="clean_db_lambda.lambda_handler",
                                         code=_lambda.Code.from_asset("clean_db/"),
                                         environment={
                                             "TABLE_NAME": table.table_name
                                         })
        clean_db_function.role.attach_inline_policy(iam.Policy(self, "CleanDBPolycy", statements=[clean_db_polycy]))
        table.grant_read_write_data(clean_db_function)


        api = apigateway.RestApi(self, "TodoApi", rest_api_name="Todo API")
        integration = apigateway.LambdaIntegration(todo_function)

        todo = api.root.add_resource("todo")
        todo.add_resource("list").add_method("GET", integration)
        todo.add_resource("create").add_method("POST", integration)
        todo.add_resource("{id}").add_method("GET", integration)
        todo.add_resource("update").add_resource("{id}").add_method("PUT", integration)
        todo.add_resource("delete").add_resource("{id}").add_method("DELETE", integration)


        rule = events.Rule(
            self, "CleanupRule",
            schedule=events.Schedule.rate(core.Duration.minutes(1))
        )
        rule.add_target(targets.LambdaFunction(clean_db_function))


app = core.App()
TodoListApiStack(app, "TodoListApiStack")
app.synth()
