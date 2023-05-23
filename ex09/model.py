"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from random import random
from exercises.ex09 import constants
from math import sin, cos, pi, sqrt


__author__ = "730607126" 


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)
    
    def distance(self, other: Point):
        """Finds the distance between two points."""
        x: float = self.x - other.x
        y: float = self.y - other.y
        return sqrt((x) ** 2 + (y) ** 2)


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.

    def tick(self) -> None:
        self.location = self.location.add(self.direction)






















    def tick(self) -> None:
        """Reassign the object's location attribute."""
        self.location = self.location.add(self.direction)
        if self.is_infected() is True:
            self.sickness += 1
            if self.sickness > constants.RECOVERY_PERIOD:
                self.immunize()

    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_vulnerable() is True:
            return "gray"
        if self.is_infected() is True:
            return "brown"
        if self.is_immune() is True:
            return "pink"
    
    def contract_disease(self) -> None:
        """This method makes a cell infected."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Checks whether a cell is vulnerable."""
        if self.sickness is constants.VULNERABLE:
            return True 
        else:
            return False
    
    def is_infected(self) -> bool:
        """Checks whether a cell is infected."""
        if self.sickness >= constants.INFECTED:
            return True 
        else:
            return False
    
    def contact_with(self, other: Cell) -> None:
        """Makes a cell contract infection after being in contact with an infected cell."""
        if (self.is_infected() is True) and (other.is_vulnerable() is True):
            other.contract_disease()
        if (other.is_infected() is True) and (self.is_vulnerable() is True):
            self.contract_disease()
    
    def immunize(self) -> None:
        """This method immunizes a cell."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Checks whether a cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True 
        else:
            return False


class Model:
    """The state of the simulation."""
    population: list[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, num_of_infections: int, num_of_immune_cells=0):
        """Initialize the cells with random locations and directions."""
        if (num_of_infections >= cells) or (num_of_infections <= 0):
            raise ValueError("Some number of the Cell objects must begin infected.")

        if num_of_immune_cells >= cells or num_of_infections >= cells:
            raise ValueError("There is an improper number of immune or infected cells in the call to model’s constructor.")

        if num_of_immune_cells < 0:
            raise ValueError("The cell is out of bounds.")
        
        if (num_of_infections + num_of_immune_cells) > cells:
            raise ValueError("You have exceeded the total.")

        self.population = []
        for i in range(cells):
            start_location: Point = self.random_location()
            start_direction: Point = self.random_direction(speed)
            cell: Cell = Cell(start_location, start_direction)
            self.population.append(cell)

        n: int = 0
        for i in range(num_of_immune_cells):
            self.population[i].immunize()
            n += 1
        
        for i in range(num_of_infections):
            self.population[n].contract_disease()
            n += 1
       
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
            self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x: float = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y: float = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle: float = 2.0 * pi * random()
        direction_x: float = cos(random_angle) * speed 
        direction_y: float = sin(random_angle) * speed
        return Point(direction_x, direction_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1.0
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1.0
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1.0
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1.0
    
    def check_contacts(self) -> None:
        """Checks whether two cells are in contact with each other."""
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                if (self.population[i].location.distance(self.population[j].location)) < constants.CELL_RADIUS:
                    self.population[i].contact_with(self.population[j])                 

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for i in range(len(self.population)):
            if self.population[i].is_infected() is True:
                return False
        return True 