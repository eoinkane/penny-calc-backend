#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { pennyCalcStack } from '../lib/cdk-stack';

const app = new cdk.App();
new pennyCalcStack(app, `penny-calc-stack-${process.env.DSAP}`);
