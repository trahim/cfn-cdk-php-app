#!/usr/bin/env python3
import os
from aws_cdk import core

from php.php_stack import PhpStack


app = core.App()
PhpStack(app, "php", env={ 'account': os.environ["CDK_DEFAULT_ACCOUNT"], 'region': os.environ["CDK_DEFAULT_REGION"] })

app.synth()
