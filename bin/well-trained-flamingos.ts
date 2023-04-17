#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { WtfJokeApi } from '../lib/wtf-joke-api-stack';

const app_prefix = 'wtf';
const app = new cdk.App();

// For now only dev
new WtfJokeApi(app, `${app_prefix}-joke-api-dev`, {
  env: { account: '417079720841', region: 'eu-west-1' },
});