# A lighTweight ConvNet: AT-Net


<a href="https://www.youtube.com/shorts/3BW1lBgtbbs" class="follow"> 
<img align="left" width="350" height="200" src="at_net.JPG"> 
</a>
This is actually a less serious weekend project called AT-Net which can be thought as a variation on Mobile-Net architecture. We start with a convolutional layer for patching then use seperable convolutions. Finally use some encoder type transformer layers. Together with some register tokens and a class token. The convolution part is highly motivated by "Patches are all you need paper". This dude will be trained on ImageNet1k dataset, we shall offer three different sizes: XXXS (1.7M params), XXS (3M params), XS (4M params), S (25M params), L (55M params).
 <h1> Our motto in coming up with AT-Net:</h1>

 <ul>
  <li> No promise to get very high accuracy,</li>
  <li> No prior assumption that exactly the same idea might have been used elsewhere,</li>
  <li> We would like to hybridize things,</li>
  <li> We do bizzare combinations for the mere reason: because we would like to!!!,</li>
  <li> In AT-Net We trust!</li>
  
</ul> 
Enjoy AT-Net!!!

# Training Details
# Optimizers
# Epochs - Batch Size


I have reached --- accuracy on ---, and guess this happened where, at home on two GPUs!!!

