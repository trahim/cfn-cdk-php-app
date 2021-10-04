#!/usr/bin/env python3

from aws_cdk import core

from php.php_stack import PhpStack


app = core.App()
PhpStack(app, "php")

app.synth()
