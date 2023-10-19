(1) Download python from this link and click the add to path option:
https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe

(2) Delete the two DELETE_ME files in the input_images and output_colors folders.

(3) Inside the color_sorting folder, click on the file explorer search bar and type 'cmd'

(4) Copy and paste these commands into cmd to install required libraries:
pip install opencv-python
pip install cvzone
pip install webcolors
pip install Pillow
pip install statistics
pip install mediapipe

Those only need to be installed one time. Now on, when running the program you can skip to step 5.

(5) After adding your images into input_images, copy and paste this into cmd to run program:
python color_sorter.py
