To decode NOAA signals  

The recorded NOAA signals are stored in the 'recorded' folder.  

In the 'compiled' folder, there are two python files - noaa_gnuradio.pyc and NOAA.py  
1.  
NOAA.py is a Python implementation of decoding NOAA signals. To run this program, go to 'compiled' folder on the terminal and  

        python NOAA.py ../recorded/NOAA17.wav

The above program requires ImageMagick package that can be installed by  

    sudo apt-get install imagemagick

Close 'Figure 1'. Resize and rotate the generated image to see the output.  
2.  
noaa_gnuradio.pyc is a compiled python file. The objective of the assignment is to generate a flowgraph on GNU radio to decode NOAA wav files. To run this compiled file,  

        python noaa_gnuradio.pyc ../recorded/090729\ 1428\ noaa-18.wav

This will create output.dat file which must be converted to png format to view the image. This can be done via  

    convert -size 2080x1024 -depth 8 gray:output.dat output.png
