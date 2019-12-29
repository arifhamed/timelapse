# Dependancies
# cv2 must be OpenCV 3
import cv2
import numpy as np
import glob
import os
import sys

### INPUT VALIDATION ###

message0 = ('Timelapse Processor V1.0',
            '- Created in Python 3.5.2',
            '- Only compatible with OpenCV 3',
            '- Currently only runs under Python shell and in .py file extension',
            '- Last updated on 28 DEC 2019',
            'Continue? (Y/N)')

[print(x) for x in message0]

enter0 = input('>>> ')
if not(enter0 in 'Yy'):
    print('Exiting software...')
    sys.exit()

name = ''
outname = ''
flag_clearframes = 1
cwd = os.getcwd()
check = 1

print()
print('Current working Directory')
print(cwd)
    
print()
print('Current items in Directory')

for i in range(len(os.listdir())):
    print('{}: {}'.format(str(i+1).zfill(3),os.listdir()[i]))
        
while check:
    print()
    print('Enter number index.')
    try:
        name = os.listdir()[int(input('>>> '))-1]
        print()
        print('Name of file: '+name)
        out_name = input('Enter name of output video (default ext: mp4): ')
        print('Clear frames after processing?')
        flag_clearframes = 0 if input('>>> ') in 'Yy' else 1
        # next task: enable customization of speed (waitKey)
        check = 0
    except:
        print('Something went wrong. Start again.')
        #sys.exit()


#-----------------------------------------------------------------------------#
### FRAME EXTRACTION ###


cap = cv2.VideoCapture(name)

frame_name = '[tlframe]_'+out_name+'_'
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
flag = 25
in_frames = total_frames//flag

message1 = ('',
            'Total frames in input video: '+str(total_frames),
            'Approximate total frames in output video: '+str(in_frames),
            '',
            'Press Space to stop process and start next process',
            '',
            'Creating timelapse_frames in current working directory',
            '## {}'.format('-'*50)
            )
[print(x) for x in message1]


frame_no = 0
prog_bar = in_frames // 50

print('## ', end='')
while(cap.isOpened()):
    frame_no += 1
    ret, img = cap.read()
    if ret==True:
        if frame_no % flag != 0: continue
        else:
            cv2.imwrite('./'+frame_name+str(frame_no).zfill(10)+'.png', img)
            if frame_no % prog_bar == 0:
                print('-', end='')
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


#-----------------------------------------------------------------------------#
### CREATING VIDEO OUTPUT ###


message2 = ('\n',
            'Collecting frames...',
            '## {}'.format('-'*50)
            )
[print(x) for x in message2]
print('## ', end='')


img_array = []
frame_no = 0

for filename in glob.glob(cwd+'/'+frame_name+'*.png'):
    try:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        frame_no += 1
        if frame_no % prog_bar == 0:
            print('-', end='')
    except:
        pass


message3 = ('\n',
            'Writing to output video...',
            '## {}'.format('-'*50)
            )
[print(x) for x in message3]
print('## ', end='')


out = cv2.VideoWriter(out_name+'.mp4',cv2.VideoWriter_fourcc(*'XVID'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
    if i % prog_bar == 0:
        print('-', end='')
out.release()

#-----------------------------------------------------------------------------#
### CLEARING PRODUCED FRAMES FROM DIRECTORY ###

frame_no = 0

message4 = ('\n',
            'Clearing frames...',
            '## {}'.format('-'*50)
            )
            
if not(flag_clearframes):
    try:
    ##    print('Clear frames?')
    ##    isit = input('>>> ')
    ##    if not(isit in 'yY'):
    ##        break
        
        [print(x) for x in message4]
        print('## ', end='')
        
        #candidates = 
        
        for filename in glob.glob(cwd+'/'+frame_name'*.png'):
            os.remove(filename)
            frame_no += 1
            if frame_no % prog_bar == 0:
                print('-', end='')
            
        
    except:
        print('Something failed. Exiting software')
        sys.exit()

print('\n\n')
print('Checking if output video exists...')

if out_name+'.mp4' in os.listdir():
    print(str(out_name+'.mp4')+' exists. Creation successful!')

print()
print('Restart Shell (Ctrl + F6) to clear cache' if 'idlelib.run' in sys.modules else '')



