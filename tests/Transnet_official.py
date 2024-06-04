import torch
from transnetv2_pytorch import TransNetV2

model = TransNetV2()
state_dict = torch.load("TransNetV2\inference-pytorch\transnetv2-pytorch-weights.pth")
model.load_state_dict(state_dict)
model.eval().cuda()

with torch.no_grad():
    # shape: batch dim x video frames x frame height x frame width x RGB (not BGR) channels
    input_video = torch.zeros(1, 100, 27, 48, 3, dtype=torch.uint8)
    single_frame_pred, all_frame_pred = model(input_video.cuda())
    
    single_frame_pred = torch.sigmoid(single_frame_pred).cpu().numpy()
    all_frame_pred = torch.sigmoid(all_frame_pred["many_hot"]).cpu().numpy()
