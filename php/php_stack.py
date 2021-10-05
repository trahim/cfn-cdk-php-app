from aws_cdk import core
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_certificatemanager as certificatemanager

class PhpStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id='vpc-1234')

        lb = elbv2.ApplicationLoadBalancer(self, "LB",
            vpc=vpc,
            internet_facing=True
        )

        listener = lb.add_listener("Listener",
            port=443,

            # 'open: true' is the default, you can leave it out if you want. Set it
            # to 'false' and use `listener.connections` if you want to be selective
            # about who can access the load balancer.
            certificates=[certificatemanager.Certificate.from_certificate_arn(self, 'cert', 'arn:aws:acm:region:account:certificate/certificate_ID_1')],
            open=True
        )

        asg = autoscaling.AutoScalingGroup(self, "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage()
        )

        listener.add_targets("ApplicationFleet",
            port=8080,
            targets=[asg]
        )