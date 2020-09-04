import {
  expect as expectCDK,
  haveResource,
  deepObjectLike,
} from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as Cdk from '../lib/cdk-stack';
import * as originalOpenApi from '../config/openapi.json';

describe('Stack Resources', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Cdk.pennyCalcStack(app, 'MyTestStack');

  it('Should have a lambda', () => {
    // THEN
    expectCDK(stack).to(haveResource('AWS::Lambda::Function'));
  });

  it('Should have an API Gateway', () => {
    // THEN
    expectCDK(stack).to(haveResource('AWS::ApiGateway::RestApi'));
  });
});

describe('Lambda Properties', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Cdk.pennyCalcStack(app, 'MyTestStack');

  it('Should run python 3.7', () => {
    // THEN
    expectCDK(stack).to(
      haveResource('AWS::Lambda::Function', {
        Runtime: 'python3.7',
      })
    );
  });

  it('Should run the correct code', () => {
    // THEN
    expectCDK(stack).to(
      haveResource('AWS::Lambda::Function', {
        Handler: 'app.src.calculate.full_amount.app.lambda_handler',
      })
    );
  });
});

describe('API Gateway', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Cdk.pennyCalcStack(app, 'MyTestStack');

  delete originalOpenApi.paths['/next-date/calculate/full-amount'].get[
    'x-amazon-apigateway-integration'
  ].uri;

  it('Should use the open api as the body', () => {
    // THEN
    expectCDK(stack).to(
      haveResource('AWS::ApiGateway::RestApi', {
        Body: deepObjectLike(originalOpenApi),
      })
    );
  });
});

test('The lambda can be invoked from the API Gateway', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Cdk.pennyCalcStack(app, 'MyTestStack');

  // THEN
  expectCDK(stack).to(
    haveResource('AWS::Lambda::Permission', {
      Action: "lambda:InvokeFunction",
      Principal: "apigateway.amazonaws.com"
    })
  );
})
