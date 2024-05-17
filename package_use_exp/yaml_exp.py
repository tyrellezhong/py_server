import yaml
import os
from collections import OrderedDict

def ordered_yaml_load(yaml_path, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path, 'r', encoding='utf-8') as stream:
        return yaml.load(stream, OrderedLoader)

def yaml_load(yaml_path):
    if bool(yaml_path) == False:
        yaml_path = os.getcwd() + "/doc/cfr_procs.yaml"
    cwd = os.getcwd()
    proc_config = os.getcwd() + "/doc/cfr_proc_config_inner.yaml"
    with open(proc_config, 'r', encoding='utf-8') as stream:
        yaml_file = ordered_yaml_load(yaml_path)
        proc_file = yaml.load(stream, yaml.Loader)
        xx = 0

