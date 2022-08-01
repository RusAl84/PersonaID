from vidgear.gears import WriteGear
import cv2

output_params = {"-vcodec": "libx264", "-crf": 0,
                 "-preset": "fast"}  # define (Codec,CRF,preset) FFmpeg tweak parameters for writer

stream = cv2.VideoCapture(0)  # Open live webcam video stream on first index(i.e. 0) device

writer = WriteGear(output_filename='Output.mp4', compression_mode=True, logging=True,
                   **output_params)  # Define writer with output filename 'Output.mp4'

# infinite loop
while True:

    (grabbed, frame) = stream.read()
    # read frames

    # check if frame empty
    # if not is grabbed:
    #     # if True break the infinite loop
    #     break

    # {do something with frame here}
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # write a modified frame to writer
    writer.write(gray)

    # Show output window
    cv2.imshow("Output Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

cv2.destroyAllWindows()
# close output window

stream.release()
# safely close video stream
writer.close()
# safely close writer