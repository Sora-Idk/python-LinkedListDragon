Hi, I'm Sora.
This project was born out of my imagination for my DSA miniproject in my second year of computer engineering. 
I found it quite easy to visualize data structures. But I think the basics could have been taught in lower grades by seeing how a linked list behaves — how nodes connect, move, get deleted, and how the structure 
dynamically changes 
So I thought, why not literally draw it?

After wanting to just display it as nodes and arrows, I remembered a cool HTML CSS animation I once saw on yt shorts of a dragon following the cursor on screen- Its body had segments like nodes and linked to each other
one behind the other- and well, I wanted to try to make it so- here we are-
Here is the link to that project that shox404 created- There is a cool interactive link on the page too if you want to check it out <https://github.com/shox404/Interactive-Dragon>
Every node is a part of the dragon’s body — the head leads, and the body gracefully follows.
Yes, the dragon is your linked list.

How it works
We start by importing pygame, math, and random @l1, initializing pygame @l3, and setting up our window and canvas surfaces @l6.
The main game window is 720×720, and all the drawing happens on an alpha-enabled canvas for transparency, which we then blit to the main screen each frame.

A small font is set up @l9 to display node data values in real-time, and we initialize a few globals:

node_count – keeps track of how long the body (linked list) is. Starts at 1 since the head always exists. @l11

selected_node – lets us highlight and view a specific node’s data. @l12 however in v1.0 I removed this functionality for time being maybe If i decide to polish this more i will add it back

Then we define the dragon’s polygons: the head, eyes, body, and wings. @l13–@l17
These are just lists of (x,y) coordinates that define the shape with respect to origin, I just took a ss of the interactive dragon and manually plotted all pixels to fit my needs in LibreCalc, You can check the attached
photos to see how lol-That was quite fun not gonna lie but - wayyy too time consuming.

The Node class
Defined at @l25
Each Node is a part of the linked list, containing:

prev and next pointers — classic doubly linked list setup.

index, data, xpos, ypos, angle, size — used for drawing and motion.

The __str__ method just returns info about the node (its data and position). @l36

Drawing the node

The draw() function @l39 is where the fun happens.

Each node’s brightness is based on its index — The closer to the tail u are  the darker the tones, giving the illusion of depth and a tail 
If it’s the head node (self.prev == None), it draws the head shape, and adds eyes 
Otherwise:

Every 3rd body segment becomes a wing (for dynamic variety). 

Other nodes draw as body scales using the p_body coordinates

If the node is selected (matches selected_node), a green outline circle is drawn #removed from v1.0
Finally, the node’s data is rendered at its center using our font and blitted to the same canvas.

Updating the node
The update() function does all motion and rotation work.
Node size smoothly decreases as its index increases, making the tail thinner. 
A smoothing factor alpha = 0.1 @l78 ensures smooth movement between frames.

#due to me playing with the code a bit after writing the part after this comment, the line numbers are not accurate, I will change them- (probably not-)

If it’s the head node, it follows the mouse position — this is your dragon’s direction. @l81–@l83
All other nodes follow their previous node, simulating a real chain motion. @l87

We then compute each node’s angle so the body faces the right direction.
Heads follow the mouse directly @l91–@l94, other nodes face toward the node before them @l95–@l98.
you can check test.py file to see how i got the math to work(mostly just googled the common ways to do it and the ai suggested this method)

Linked List Operations
We create the head node right after the class definition by taking user input for its data value. @l101

Insert
insert(data) @l103
Finds the tail node, attaches a new one to its end, and adjusts its position to appear behind it.
Reindexes and increments node_count. @l117

Search
search(target) @l121
Traverses from head until the value is found and prints its index. @l124–@l129

Delete
delete(target) @l132
Removes a node safely from the list. Works for:

Middle nodes (adjusts both pointers). @l139
Head (moves head forward). @l143
Tail (sets the previous node’s next to None). @l146

Then reindexes the whole list to keep indices correct @l151.
If the element wasn’t found or list is too short, prints an error. @l156

Utility functions
rotate_point(px, py, angle_deg) @l159 rotates the dragon’s polygon points for proper body alignment.
display() @l164 prints the linked list to the terminal (index, data, coords).
show_menu() @l171 just prints command options for user interaction.

Input & Event Handling
input_handler(inp) @l175 lets you:
menu → shows available commands
insert → add new node with integer data
search → find a node by value
print → display all nodes in terminal
delete → remove a node by value

All of these commands directly call the linked list functions. @l176–@l193

Keybinds
Handled inside keypress_handler(key) @l195:
Q → Quit the program.
UP / DOWN → Navigate between nodes to highlight them visually.
R → Insert random node data for fun.

Mouse clicks
Handled by click_handler(button) @l207
Right-click (button 3) opens an input prompt for typing commands.

Game loop & drawing
All events are passed through event_handler(event) @l211.
The main loop starts at @l220.

Inside the loop:
The canvas is cleared every frame with a background color (113,90,90) @l223.
Then each node’s draw() and update() are called in sequence @l227–@l232.
The canvas is blitted to the window @l236.

Frame rate is locked to 60 FPS @l238.
pg.display.flip() updates the window.

Finally, all pending pygame events are processed @l241.
And that’s it — your linked list dragon lives, breathes, and flies across your screen.

Summary
Each part of the dragon represents a node in a doubly linked list, and you can:
Add nodes (insert)
Search nodes (search)
Delete nodes (delete)
Print them (print)
All visually represented in motion.

The head follows your mouse.
The body follows the head.
The list follows your commands.

That’s the core idea — making data structures alive.

Future plans
Add color transitions based on node data.
Visualize node deletion animations (fade out / dissolve).
Add “split” and “merge” operations as dragon transformations.
Maybe even add sound or particle effects.

Until next time. o7
