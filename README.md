![BrickBoyColor_sm](https://github.com/lc-jrx/BrickBoyColor/assets/133227013/01c12322-218b-4a48-860d-f83e447a8038)

# PortaBrick Arcade
This project is about a fully working portable arcade gaming console made from 100% pure LEGO® and Python/MicroPython. This project is now ready to vote for at LEGO® Ideas platform. If you want to make the **PortaBrick Arcade** a real product please vote for at [ideas.lego.com](https://ideas.lego.com/projects/53e8d771-166c-4a35-85d3-25e3512eb799).

***

### General Info
Basis for the project are the electronic components from LEGO® Spike Prime and elements from LEGO® Technic. The code is written in Python/Micropython and is based upon [Pybricks](http://pybricks.com) project – thanks a lot! The project was carried out as part of the Bachelor programme "[Online-Studiengang Medieninformatik](https://informatik.th-brandenburg.de/studium/bachelorstudiengaenge/online-studiengang-medieninformatik/)" (Online Study Program Media Informatics)" at the [University of Applied Sciences Brandenburg](https://www.th-brandenburg.de). 

### Games & How to play

Currently two arcade games are implemented for the PortaBrick Arcade. The first game is "BrickPong" – an implementation of the the classic arcade game Pong. The second one named "BrickSnake" is an implementation of the well-known game "Snake" from earlier Nokia phones.


#### Program control
The PortaBrick Arcade is controlled by the four buttons of the hub. The Bluetooth button serves as a stop and ends the whole program sequence. The center button serves as an input button and confirms the selected choice in menus. The selection itself is made using the two arrow keys.

#### Game controls
After starting the games, the input is done via the two game controllers.

In BrickSnake, the left controller makes the snake turn left (counterclockwise). The right controller accordingly makes the snake turn to the right (clockwise).

In BrickPong, the two controllers steer the left tennis racket. The left game controller makes the racket move to the left (i.e. upwards), right correspondingly to the right (i.e. downwards). The game controllers have a staggered sensitivity. A slight pressure moves the racket pixel by pixel. Stronger pressure on the controllers moves the racket two or more pixels in the respective direction. The right tennis racket is steered by the computer.

### Known Bugs
#### Snake
No known bugs.
#### Pong
I: When a higher game speed aka difficulty level is selected, the movement of the ball is not correct and not predictable. Also, in this case, the rules for the upper and lower boundaries of the playing field do not work correctly.

II: The "Hard Game" setting has no effect on the size of the tennis rackets at the low resolution of 6x6 pixels.

### Future or possible expansion and further development
- rework of main menu
- addition of more games like Tetris, Space Invaders or Pac Man
- wireless connection between two PortaBrick Arcade for multi-player games
- extension of the PortaBrick Arcade to a stationary arcade machine
- port to LEGO® native Python as used in Spike app 
### Licence
The PortaBrick Arcade, the PortaBrick Arcade software and the PortaBrick Arcade games are licensed under the [MIT License](LICENSE).

### Disclaimer
LEGO® is a trademark of the LEGO Group of companies which does not sponsor, authorize or endorse this project.
