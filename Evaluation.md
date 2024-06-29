# Evaluation Task 30. June
#### Group IVADL12

### Assignment Overview

Our task for this assignemnt was to test the performance of our system/model, by choosing one video and then providing some queries. For this we randomly chose video 107 (V3C100/00107), then we took 6 random screenshots from the video 
and tested these as image queries. We also tried to provide text queries, which are based on the 6 screenshots. Further for the similarity search regarding the text queries, we tried to compare them to text embeddings,
 which were created with Blip(base) and Blip2 and also simply with the image embeddings, which Clip created for us. 

### Evaluation of Image Queries

This is the first screenshot we used. It was taken at about 47 seconds into the video.
Our results were the following:

On the left you see first the query image, than underneath it the best similarity value, which is good, but the timestamp is not the correct one. But on the right there is a really good fit, which had the second or third highest similarity.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/e35e5795-1e0b-4869-96de-39c94a49eb82" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/b51a1743-c091-4cb4-b703-24a572f3c891" alt="Image 2" width="45%" height="50%">
</div>
<br><br>

The second screenshot was taken at about 1 minute and 6 seconds:
On the left we have the best similarity and on the right the second best, which are both in a very good area looking at the time stamps.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/84eccba6-175d-4eb0-8dd7-f0db95e80db7" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/dafc8077-6cb5-4465-a535-2d9d1812dd31" alt="Image 2" width="45%" height="50%">
</div>
<br><br>


The third screenshot was taken at about 1 minute and 10 seconds:

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/42b73bfa-9036-4775-8e22-15a9d58153df" alt="Image 1" width="60%" height="50%" style="margin-right: 0px;">
</div>
<br><br>
The fourth screenshot was taken at about 3 minutes and 49 seconds:

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/472f22b5-b31c-47fd-baac-9ddb0d46f081" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>

<br><br>
The fifth screenshot was taken at about 3 minutes 55 seconds:
This was an example were only a somewhat similar frame was found, which is in the same video, but the timestamp is far away at about 2 minutes 35 seconds. The actual result can still be found through the video playback.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/5be5c9fe-8c47-4310-9620-95a7d2e95624" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>
<br><br>
The last screenshot was taken at about 4 minutes 28 seconds:

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/e9032ed9-a90f-4170-aa46-c11996369644" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>


As it is visible, for most image queries, a really good fit was found where the time stamp is close to the original one as well. I again want to clarify that all screenshots were taken at random and were not selected to be close to scene changes.
The fact that the screenshots were taken randomly can also be seen in example five, where the scene is really short and has no transition prior to it, therefore no good fit exists.

### Evaluation of Text Queries

As already stated in the Assignment Overview, we tried to now provide text queries, which describe the previously taken screenshots.

The first text query is the following:
On the left you can see the query and the result when comparing it to the image embedding. On the right is the comparison to the text description from Blip2.
As you can see the Blip(base) description is not as good, as here we do not find a good timestamp, with Blip2 on the other side we find a good time stamp rather fast.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/d1f6437b-6a64-4d44-b8ac-a42793e8ef2b" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/f6f8f5d9-b570-4e02-a13d-51b736564a88" alt="Image 2" width="45%" height="50%">
</div>
<br><br>
The second text query:
Here the left one shows the comparison with the description of Blip2 and the right one with Blip. Below you can see a try with taking the same query as for Blip2.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/116faf67-e9f0-4edf-a188-8753f4b1f0d6" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/25ac3594-b023-434d-a12f-ba7b850586ba" alt="Image 2" width="45%" height="50%">
</div>
<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/9244eb16-00e8-41ed-a417-e1d378048ed8" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>
<br><br>

The thrid text query:
On the left we again have Blip2 and on the right Blip with the same query. Below is the result when using the same query and comparing to the image embedding.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/6d4a4a08-0764-439b-a325-228a6fe8cacd" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/334d9a64-b33b-4b3d-ba19-581505024526" alt="Image 2" width="45%" height="50%">
</div>
<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/41eada2a-94a7-4c61-bb8f-2a2da1152af5" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>
<br><br>

The fourth text query:
On the left we again have Blip2 and on the right Blip with the same query. Below is the result when using the same query and comparing to the image embedding.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/56be3970-7ab7-4dcb-9c67-ac64c75d2f83" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/0309c7f1-82af-470c-b6f0-9690edf8dcca" alt="Image 2" width="45%" height="50%">
</div>
<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/e002dc6c-cba0-49bf-b7c3-8db8e510628e" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>
<br><br>

The fifth text query:
Here on the left and right were compared to the image embedding, where the left is the best and right the second best similarity, but the right one has actually the nearly perfect time stamp. Below is a comparison with the Blip text embedding and here Blip2 gave the same result.

<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/6f131487-e394-468a-87ce-1226355a3ad2" alt="Image 1" width="45%" height="50%" style="margin-right: 0px;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/5950b082-44a4-4c65-b43c-4739a89fe763" alt="Image 2" width="45%" height="50%">
</div>
<div style="display: flex;">
  <img src="https://github.com/bwesse/video_analysis/assets/150476303/f2f0416e-7955-4d7a-bd2a-e9c592d0487d" alt="" width="60%" height="50%" style="margin-right: 0px;">
</div>
<br><br>

One thing that can be observed here is, that the results where the text queries were compared to the image embeddings work quite well, but the similarity score is rather low. 
Another observation is, that Blip2 creates better/more detailed description and also uses the text that is visible in keyframes, but it's still not perfect.

