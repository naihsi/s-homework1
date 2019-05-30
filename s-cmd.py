
import boto3
from pprint import pprint
import time

# #### ##### ##### #####


def ec2_cli():
    client = boto3.client('ec2', region_name='us-west-2')
    return client


# #### ##### ##### #####


def list_inst():
    _filters = []
    _res = ec2_cli().describe_instances(Filters=_filters)

    pprint(_res)


def query_state(inst_id):
    _filters = [
        {
            "Name": "instance-id",
            "Values": [
                inst_id
            ],
        }
    ]
    _res = ec2_cli().describe_instances(Filters=_filters)

#    pprint(_res)

    _state = _res["Reservations"][0]["Instances"][0]["State"]["Name"]
#    print(_state)
    return _state


def wait_for(state, inst_id):
    while(True):
        _state = query_state(inst_id)
        if _state == state:
            print("got {}".format(state))
            break

        print("waiting for {} (now is {})".format(state, _state))
        time.sleep(5)


def terminate_inst(inst_id, dryrun=False):
    _ids = [
        inst_id,
    ]
    _res = ec2_cli().terminate_instances(InstanceIds=_ids, DryRun=dryrun)
    pprint(_res)


def create_inst(branch_name, dryrun=False):
    _block = [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': 8,
                'VolumeType': 'gp2'
            },
        },
    ]
    _imageId = "ami-07a0c6e669965bb7c"
    _key = "service"
    _instanceType = "t2.micro"
    _max = 1
    _min = 1
    _monitoring = {
        'Enabled': False,
    }
    _sgids = [
        "sg-0082b64c2f5e30dc6",
    ]
    _subnet = "subnet-089cbf40921c9c705"

    _tags = [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'role',
                    'Value': 'service'
                },
                {
                    'Key': 'branch',
                    'Value': branch_name
                },
            ]
        },
    ]

    _res = ec2_cli().run_instances(
        BlockDeviceMappings=_block,
        ImageId=_imageId,
        KeyName=_key,
        InstanceType=_instanceType,
        MaxCount=_max,
        MinCount=_min,
        Monitoring=_monitoring,
        SubnetId=_subnet,
        SecurityGroupIds=_sgids,
        TagSpecifications=_tags,
        DryRun=dryrun
    )

    _inst_id = _res["Instances"][0]["InstanceId"]

    pprint(_res)
    print("new inatnce: {}".format(_inst_id))

    return _inst_id


# #### ##### ##### #####

def pass_dryrun(func, params):
    try:
        func(*params)
    except Exception as e:
        _msg = str(e)
        if "Request would have succeeded, but DryRun flag is set." in _msg:
            return True
        else:
            return False


def test():
    print("init")
#    list_inst()
#    _inst_id = "i-0d9203c6d734e76c7"
    _branch_name = "feature1"

    # dryrun a function
    _res = pass_dryrun(create_inst, (_branch_name, True))
    print("dryrun passed: {}".format(_res))

    # create an instance
    _inst_id = create_inst(_branch_name)
    print("new inatnce: {} (branch: {})".format(_inst_id, _branch_name))

    # query instance
    _state = query_state(_inst_id)
    print("state: {}".format(_state))

    # query an instance until it reached a state
    wait_for("running", _inst_id)

    # terminate an instance
#    _inst_id = "i-0a4236bbd85ff30d9"
    terminate_inst(_inst_id)
    wait_for("terminated", _inst_id)
#    _inst_id = "i-000a8e64eda4f4df6"


if __name__ == "__main__":
    test()
