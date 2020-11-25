# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import tempfile
import os
import json
from pathlib import Path
WORKDIR_HANDLER = tempfile.TemporaryDirectory()
os.environ["TF_DUMP_GRAPH_PREFIX"] = WORKDIR_HANDLER.name
os.environ["TF_CPP_MIN_VLOG_LEVEL"] = "4"
from superscaler.scaler_graph.IR.conversion import tf_adapter  # noqa: E402
from superscaler.scaler_graph.IR import operator  # noqa: E402


def test_graph_io():
    '''test:
        import sc graph from tf pbtxt file;
        export sc graph into tf pbtxt file;
    '''
    tf_pbtxt_path = os.path.join(os.path.dirname(__file__), "data",
                                 "SimpleCNNRun.pbtxt")
    sc_graph = tf_adapter.import_graph_from_tf_file(tf_pbtxt_path)
    sc_graph_serialization_file = \
        os.path.join(os.path.dirname(__file__),
                     "data", "SimpleCNNRun.json")
    file = Path(sc_graph_serialization_file)
    assert (len(sc_graph.nodes) == 130)
    assert (json.loads(file.read_text()) == json.loads(sc_graph.json()))


def test_remove_nodes():
    '''test:
        remove node and edge
    '''
    tf_pbtxt_path = os.path.join(os.path.dirname(__file__),
                                 "data", "MatmulRun.pbtxt")
    sc_graph = tf_adapter.import_graph_from_tf_file(tf_pbtxt_path)
    node_names = [node.name for node in sc_graph.nodes]
    for node_name in node_names:
        node = sc_graph.get_node_by_name(node_name)
        sc_graph.remove_node_and_edge(node)
    assert (len(sc_graph.nodes) == 0 and len(sc_graph.edges) == 0)


def test_insert_node():
    tf_pbtxt_path = os.path.join(os.path.dirname(__file__),
                                 "data", "MatmulRun.pbtxt")
    sc_graph = tf_adapter.import_graph_from_tf_file(tf_pbtxt_path)
    edge = sc_graph.get_node_by_name("MatMul").in_edges[0]  # x --> matmul
    sc_graph.remove_edge(edge)

    sc_op = operator.AllreduceOp()
    input_node_idxes = []
    input_node_idxes.append((edge.src_node, edge.src_idx))
    attrs = {}
    attrs["tensor_name"] = edge.src_node.name + "_allreduce"
    attrs["T"] = edge.src_node.attrs["T"]
    attrs["reduction"] = "sum"
    attrs["num_devices"] = "2"
    node_name = edge.src_node.name + "_allreduce"
    node = sc_graph.add_node_and_edge(node_name, sc_op, input_node_idxes, 1,
                                      attrs)
    sc_graph.add_edge(node, 0, edge.dest_node, edge.dest_idx)

    inserted_allreduce_file = \
        os.path.join(os.path.dirname(__file__),
                     "data", "MatmulRunAllreduce.json")
    file = Path(inserted_allreduce_file)
    assert (file.read_text() == sc_graph.json())