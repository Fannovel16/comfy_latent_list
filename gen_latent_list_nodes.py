MAX_RESOLUTION = 8192
import torch
class EmptyLatentList:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "width": ("INT", {"default": 512, "min": 64, "max": MAX_RESOLUTION, "step": 64}),
                              "height": ("INT", {"default": 512, "min": 64, "max": MAX_RESOLUTION, "step": 64}),
                              "batch_count": ("INT", {"default": 1, "min": 1, "max": 64}),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})}},
    RETURN_TYPES = ("LATENT_LIST",)
    FUNCTION = "generate"

    CATEGORY = "latent"

    def generate(self, width, height, batch_count = 1, batch_size=1):
        latent_list = []
        for i in range(batch_count):
            latent = torch.zeros([batch_size, 4, height // 8, width // 8])
            latent_list.append({"samples":latent})
        return (latent_list, )