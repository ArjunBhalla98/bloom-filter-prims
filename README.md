# A Memory Efficient Adaptation of Prim's Algorithm
In this project, we use bloom filters in Prim's algorithm to approximate MST's for (ideally) massive graphs. Empirically, we have achieved this with ~93% memory reduction from Prim's algorithm, with a < 0.3% error rate.

To show some real applications of this, here are some of the results of running basic image segmentation using simple MST clustering methods - first with Prim's algorithm, then with our method. We see that empirically, both methods are incredibly similar.

The images are from the <a href="https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/" > BSDS 300 </a> (Berkeley Image Segmentation Dataset), and the MST clustering is a basic implementation based on <a href="https://github.com/jakevdp/mst_clustering/"> Jake Vanderplas' MST clustering library. </a> However, instead of using the L2 norm as a distance function between two nodes (pixels), I used the L2 norm's square, because this made it easier to find better threshold points for the segmentation task.  

<br>

|                   Original Image                   |      Prim's Algorithm, basic MST clustering       |          Our method, basic MST clustering          |
| :------------------------------------------------: | :-----------------------------------------------: | :------------------------------------------------: |
|  <img src="./results/images/img%20one/truth.jpg">  |  <img src="./results/images/img%20one/test.jpg">  |  <img src="./results/images/img%20one/bloom.jpg">  |
|  <img src="./results/images/img%20two/truth.jpg">  |  <img src="./results/images/img%20two/test.jpg">  |  <img src="./results/images/img%20two/bloom.jpg">  |
| <img src="./results/images/img%20three/truth.jpg"> | <img src="./results/images/img%20three/test.jpg"> | <img src="./results/images/img%20three/bloom.jpg"> |
| <img src="./results/images/img%20four/truth.jpg">  | <img src="./results/images/img%20four/test.jpg">  | <img src="./results/images/img%20four/bloom.jpg">  |

I chose the last one particularly because of the stark difference in the foreground and background, and the fact that there is only one real subject (the plane). This served to more clearly highlight that there is a minor difference in our method and that our method can cause small errors, but they importantly do not really visually affect the result and as such are negligible in practice.

## Set up
```pip install -r requirements.txt```
