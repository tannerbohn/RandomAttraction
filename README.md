# RandomAttraction
An abstract look at attraction in a population.

In this simulation, people are represented as randomly coloured circles, and
every person is randomly attracted to another person (indicated by a line).

To make the simulation more interesting, every person moves towards the person
they are attracted to, and away from everyone else.

Every once in a while (the frequency can be set at the top of the Person class),
the "attractor" of an individual will change. You can turn this random switching
on and off by right-clicking the canvas. When switching is disabled, every circle
will have a thin red outline.

If you click on a person, you can toggle their ability to move (when they are fixed,
they turn dark red).

The people move around on a toroidal surface (so moving beyone the top or bottom
takes you to the bottom or top and similarly for left and right edges). The center
of mass of the population is constantly tracked and the map is centered.
