''' This program draws a neusis called a cissoid, needed for doubling the cube 
    in a point-wise way, as specified by Diocles around 180 BC.'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Take user input on the amount of wanted points and iniate global variables based on that
num_points = int(input("Please specify the number of points Theta you would like to generate: "))

if num_points < 7:
    interval = 400
elif num_points < 20:
    interval = 150
else:
    interval = 50

ann_list = []
theta_list = []
num_frames = (num_points * 5) + num_points
last_frame = num_frames - num_points




# Animation loop
def update_lines(frame, lines, last_frame):
    
    if frame > last_frame:
        return lines, last_frame

    # Take a random number on LD and draw line HZ
    if frame % 5 == 0 and len(ann_list) != 2 and frame != last_frame:    
        rand = 10 * np.random.random()
        rand_y = -np.sqrt(10**2 - rand**2)
        lines[0].set_data([rand, rand], [0, rand_y])
        
        ann_list[0].set_position((rand + 0.1, 0 + 0.15))
        ann_list[0].set(visible=True)
        ann_list[1].set_position((rand + 0.1, rand_y - 0.8))
        ann_list[1].set(visible=True)
    
    # Dummy function to circumvent the weird double 0 start of funcanimation
    if frame == 0 and len(ann_list) == 2:
        ann1 = ax.annotate('\u0397', ( 0.1, 0 + 0.15), size=13, visible=False) # Eta
        ann_list.append(ann1)

    # Draw the the second line KZ mirrored on the left side of the circle   
    if frame % 5 == 1: 
        xx, yy = lines[0].get_data()
        lines[1].set_data([-xx[0], -xx[1]], [0, yy[1]])

        ann_list[2].set_position((-xx[0] + 0.1, 0 + 0.15))
        ann_list[2].set(visible=True)
        ann_list[3].set_position((-xx[0] + 0.1, yy[1] + 0.15))
        ann_list[3].set(visible=True)
        
    # Draw the diagonal ED to find Theta
    if frame % 5 == 2:
        xx, yy = lines[1].get_data()
        lines[2].set_data([xx[0], 10], [yy[1], 0])

    # Calculate and draw point Theta
    if frame % 5 == 3:
        xx, yy = lines[0].get_data()

        KD = xx[0] + 10
        KE = -yy[1]
        HD = 10 - xx[0]
        HT = -(HD/(KD/KE))

        theta_list.append([xx[0], HT])
        # If you want to save an animation the color here should be black (color='black')
        # and you can decrease the size of the dots (s=(...)) if you want to animate a curve with a lot of points
        ax.scatter(xx[0], HT, color='red', s=(8))   
        ann_list[4].set_position((xx[0] + 0.1, HT - 0.8))
        ann_list[4].set(visible=True)

    # Cleanup for a new loop
    if frame % 5 == 4: 
        for line in lines:
            line.set_data([], [])
        for ann in ann_list:
            ann.set(visible=False)

    # Draw the cissoid through the points Theta
    if frame == last_frame:
        x_list = sorted([th[0] for th in theta_list] + [0] + [10])
        y_list = sorted([th[1] for th in theta_list] + [0] + [-10])
        ax.plot(x_list, y_list, c='purple', lw=1.5)

    return lines, last_frame

# Create figure to draw on
fig = plt.figure()
fig.clear()
# ax = plt.axes(rasterized=1)
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Prebuild invisible annotations with dummy positions
ann_list.append(ax.annotate('\u0397', (0.1, 0.15), size=13, visible=False)) # Eta
ann_list.append(ax.annotate('\u0396', (0.1, 0.8), size=13, visible=False)) # Zeta
ann_list.append(ax.annotate('\u039A', (0.1, 0.15), size=13, visible=False)) # Kappa
ann_list.append(ax.annotate('\u0395', (0.1, 0.15), size=13, visible=False)) # Epsilon
ann_list.append(ax.annotate('\u0398', (0.1, 0.8), size=13, visible=False)) # Theta


# Create empty lines
lines = [ax.plot([], [], color='black')[0] for _ in range(3)]

# Draw circle and add to figure
circle = plt.Circle((0, 0), radius=10, fill=0, lw=1.5)
plt.gca().add_patch(circle)

# Draw static lines and annotate
ax.plot([0, 0], [10, -10], c='black', lw=1.5)
ax.annotate('\u0391', (0.1, 10.15), size=13) # Alpha
ax.annotate('\u0392', (0, -10 + 0.15), size=13) # Beta

ax.plot([-10, 10], [0, 0], c='black', lw=1.5)
ax.annotate('\u0393', (10, 0), size=13) # Gamma
ax.annotate('\u0394', (-10 + 0.15, 0.15), size=13) # Delta

ax.annotate('\u039B', (0.1, 0.15), size=13) # Lambda

plt.axis('scaled')
# plt.grid(visible=1, ls='dotted')

ani = animation.FuncAnimation(fig, update_lines, frames=num_frames, fargs=(lines, last_frame), interval=interval, repeat=False, save_count=num_frames)

'''Uncomment the lines below to save the animation as a gif
   Also note that you need to change the color of the Theta dot above to black
   for the animation saver to properly work (don't ask me why)'''
# writergif = animation.PillowWriter(fps=1000/interval) 
# ani.save(f"cissoid_{num_points}points.gif", writer=writergif)

plt.show()


