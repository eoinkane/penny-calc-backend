import * as cdk from '@aws-cdk/core';
import * as AWSlambda from '@aws-cdk/aws-lambda';
import * as AWSapigateway from '@aws-cdk/aws-apigateway';
import * as AWSIam from '@aws-cdk/aws-iam';
import * as originalOpenApi from '../config/openapi.json';

export class pennyCalcStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // defines an AWS Lambda resource
    const lambda = new AWSlambda.Function(
      this,
      `penny-calc-full-amount-lambda-${process.env.DSAP}`,
      {
        runtime: AWSlambda.Runtime.PYTHON_3_7,
        code: AWSlambda.Code.fromAsset('build'),
        handler: 'app.src.calculate.full_amount.app.lambda_handler',
        functionName: `penny-calc-full-amount-lambda-${process.env.DSAP}`,
      }
    );


    const lambdaName = lambda.functionName;

    const openApiString = JSON.stringify(originalOpenApi);
    const openApiStringModified1 = openApiString.replace(
      'replace-uri',
      `arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:710912430193:function:${lambdaName}/invocations`
    );
    const openApiModified = JSON.parse(openApiStringModified1);

    const api = new AWSapigateway.SpecRestApi(
      this,
      `penny-calc-api-${process.env.DSAP}`,
      {
        apiDefinition: AWSapigateway.ApiDefinition.fromInline(openApiModified),
        deploy: true,
        deployOptions: {
          stageName: process.env.DSAP,
        },
      }
    );

    lambda.grantInvoke(new AWSIam.ServicePrincipal('apigateway.amazonaws.com'));
  }
}
