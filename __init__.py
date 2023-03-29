from . import latent_nodes
from . import k_sampler_nodes
import copy

NODE_CLASS_MAPPINGS = {}
for latent_nodes, latent_node_name in \
        list(map(lambda latent_node_name: (latent_nodes, latent_node_name), filter(lambda x: "Latent" in x, dir(latent_nodes)))) + \
        [(k_sampler_nodes, "KSampler"), (k_sampler_nodes, "KSamplerAdvanced")]:
    latent_node_class = getattr(latent_nodes, latent_node_name)
    latent_node = latent_node_class()

    class LatentListWrapper():
        @classmethod
        def INPUT_TYPES(s):
            input_types = latent_node_class.INPUT_TYPES()
            for key in input_types["required"]:
                if input_types["required"][key][0] == "LATENT":
                    t = list(input_types["required"][key])
                    t[0] = "LATENT_LIST"
                    input_types["required"][f"{key}_list"] = tuple(t)
                    break
            return input_types

        RETURN_TYPES = latent_node.RETURN_TYPES
        CATEGORY = latent_node.CATEGORY

        FUNCTION = "process_latent_list"

        def __init__(self):
            self.MAIN_FUNCTION = latent_node_class.FUNCTION

        def process_latent_list(self, **kwargs):
            for input_key in kwargs.keys():
                if "_list" in input_key:
                    latent_list_key = input_key
                    break
            assert latent_list_key is not None

            def process_latent(latent):
                main_kwargs = copy.deepcopy(kwargs)
                main_kwargs[latent_list_key.replace("_list", '')] = latent
                del main_kwargs[latent_list_key]
                return getattr(latent_node, self.MAIN_FUNCTION)(**main_kwargs)
            return (list(map(process_latent, kwargs[latent_list_key])), )

    NODE_CLASS_MAPPINGS[latent_node_name.replace(
        "Latent", "LatentList")] = LatentListWrapper