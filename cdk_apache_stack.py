from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

# Variables
ec2_type = "t2.micro"
key_name = "masterkey"

# Read user_data
with open("user_data.sh", encoding="UTF-8") as f:
    user_data = f.read()

class CdkApacheStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public_subnet", subnet_type=ec2.SubnetType.PUBLIC)]
            )
        
        # Get AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Create EC2 Instance
        host = ec2.Instance(self,"myEc2",
            instance_type=ec2.InstanceType(
                instance_type_identifier=ec2_type),
            machine_image=amzn_linux,
            vpc=vpc,
            key_name=key_name,
            user_data=ec2.UserData.custom(user_data)
        )
    
        # Configure EBS Volume:
        host.instance.add_property_override("BlockDeviceMappings", [{
            "DeviceName": "/dev/xvda",
            "Ebs": {"VolumeSize": "30"}
        }
        ])
        
        # Configuring Security Group SSH/HTTP access to instance
        host.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22), "Allow ssh access")
        host.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Allow http access")
        
        CfnOutput(self, "Output",
                  value=host.instance_public_ip)