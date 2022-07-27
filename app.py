#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_apache.cdk_apache_stack import CdkApacheStack

app = cdk.App()
CdkApacheStack(app, "CdkApacheStack")

app.synth()
