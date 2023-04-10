# motion
Simple movement detection based on frame subtraction using OpenCV

- image processing
- first frame storage
- subtraction between the current frame and the first one
- draw boxes on the regions with movement occurence

The parameters used for detection, such as treshold or scaling can be tweaked in the code.

## Input

Video file (optional) and minimum window size in pixels (optional, default = 500), passed as arguments on the command line.
- If no video is given, the program reads from the webcam.

## Output

Real-time frames, with bounding boxes drawed on the regions with movement occurences, and a flag warning that movement occured.

## Tools

- Python 3.10
- OpenCV
- Visual Studio Code
- Webcam

## Execution

`python motion.py </path/to/video.mp4> [-m <minimum window size>]`
