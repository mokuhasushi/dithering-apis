# Background Art

The idea is to have some pcg for background images, and daily (or weekly) serve them on the website or make them public. 

1. check if this exists already 
2. look for image processing libraries 
3. implement some algorithms
4. profit 

## Algorithms ideas

### Dithering
Upload an image (or take a random one from a random images website/API)
Apply a dithering algorithm (either implemnt it for the fun or use an existing one)
Done

### Rolling average
Transform every pixel assigning to it the average of the following x (e.g: 10)
Another option could be to assign to every pixel in a x times x square the same value (averaged) to obtain a coarser effect.
Very big square could make for nice graphics
Coarse squares could also be obtained by scaling down the quality 
To have a more digital effect chose the top colors (or some nice ones) and assign to every pixel closest Hamming palette's