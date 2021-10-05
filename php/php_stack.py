from aws_cdk import core
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_certificatemanager as certificatemanager

class PhpStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=self.node.try_get_context("vpc_id"))

        lb = elbv2.ApplicationLoadBalancer(self, "LB",
            vpc=vpc,
            internet_facing=True
        )

        listener = lb.add_listener("Listener",
            port=443,
            certificates=[certificatemanager.Certificate.from_certificate_arn(self, 'cert', self.node.try_get_context("cert_arn"))],
        )

        asg = autoscaling.AutoScalingGroup(self, "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.lookup(name=self.node.try_get_context("ami_id"), owners=[self.account]),
            min_capacity=5,
            max_capacity=100
        )

        listener.add_targets("ApplicationFleet",
            port=8080,
            targets=[asg]
        )

        asg.scale_on_cpu_utilization("KeepSpareCPU",
            target_utilization_percent=70
        )