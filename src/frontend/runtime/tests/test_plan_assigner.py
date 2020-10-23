import os
import json
from plan_assigner import PlanAssigner


def get_communication_plan(path, device_count):
    # Parser communication_plan from path
    communication_plan = []
    for i in range(device_count):
        sub_path = os.path.join(path, "superscaler_" + str(i) + ".json")
        plan = json.load(open(sub_path, 'r'))
        communication_plan.append(plan)
    return communication_plan


def test_plan_assigner():

    # Init PlanAssigner class
    pb = PlanAssigner()

    # Wrong test
    assert(pb.assign(None, None) is None)
    # Empty test
    assert(pb.assign(None, {}) is None)

    # Init inputs of PlanAssigner
    deployment_setting = {"1": "10.0.0.21"}
    communication_plan = get_communication_plan(os.path.join(
        os.path.dirname(__file__), 'data'), 2)

    assigned_communication_plan =\
        pb.assign(communication_plan, deployment_setting)

    # Check the correctness of output
    output_path = os.path.join(
        os.path.dirname(__file__), "data/assigned_communication_plan.json")

    assigned_communication_plan_ref = json.load(open(output_path, 'r'))

    assert(assigned_communication_plan == assigned_communication_plan_ref)