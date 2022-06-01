# iworkout pose estimation (video)

# Capture pose landmarks

Mediapipe offers a pretty neat way to acquire landmark coordinates -> mp.solutions.pose.PoseLandmark

```bash

import mediapipe as mp

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Use lm and lmPose as representative of the following methods.
lm = keypoints.pose_landmarks
lmPose = mp_pose.PoseLandmark

# Acquire the landmark coordinates.
l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

```

# Find angles

We need two key components to calculate angles for both sides.

```bash

# finAngle
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Calculate angles.
left_inclination = findAngle(l_shldr_x, l_shldr_y, l_elbow_x, l_elbow_y)
right_inclination = findAngle(r_elbow_x,r_elbow_y, r_shldr_x, r_shldr_y)

```

# Good pose vs bad pose

Use OpenCV to draw lines between joints. Line color turns into red when bad pose is detected.

```bash

if (left_inclination + right_inclination) <= 200:
    bad_frames = 0
    good_frames += 1

    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
    cv2.putText(image, str(int(left_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
    cv2.putText(image, str(int(right_inclination)), (r_shldr_x + 10, r_shldr_y), font, 0.9, light_green, 2)

    cv2.line(image, (l_shldr_x, l_shldr_y), (l_elbow_x,l_elbow_y), green, 4)
    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
    cv2.line(image, (r_shldr_x,r_shldr_y), (r_elbow_x,r_elbow_y), green, 4)
    cv2.line(image, (r_shldr_x,r_shldr_y), (r_shldr_x,r_shldr_y - 100), green, 4)

else:
    good_frames = 0
    bad_frames += 1

    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
    cv2.putText(image, str(int(left_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
    cv2.putText(image, str(int(right_inclination)), (r_shldr_x + 10, r_shldr_y), font, 0.9, red, 2)

    # Join landmarks.
    cv2.line(image, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), red, 4)
    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
    cv2.line(image, (r_shldr_x,r_shldr_y), (r_elbow_x,r_elbow_y), red, 4)
    cv2.line(image, (r_shldr_x,r_shldr_y), (r_shldr_x,r_shldr_y - 100), red, 4)

```

# Good pose time vs bad pose time

```bash

# Calculate the time of remaining in a particular posture.
good_time = (1 / fps) * good_frames
bad_time =  (1 / fps) * bad_frames

if good_time > 0:
    time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
    cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
else:
    time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
    cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

```
