---
layout: post
title: "Low Level Design Snake Game"
date: 2025-08-07
---
# Snake Game
https://leetcode.com/problems/design-snake-game/description/
## 353. Design Snake Game
Design a Snake game that is played on a device with screen size height x width. Play the game online if you are not familiar with the game.

The snake is initially positioned at the top left corner (0, 0) with a length of 1 unit.

You are given an array food where food[i] = (ri, ci) is the row and column position of a piece of food that the snake can eat. When a snake eats a piece of food, its length and the game's score both increase by 1.

Each piece of food appears one by one on the screen, meaning the second piece of food will not appear until the snake eats the first piece of food.

When a piece of food appears on the screen, it is guaranteed that it will not appear on a block occupied by the snake.

The game is over if the snake goes out of bounds (hits a wall) or if its head occupies a space that its body occupies after moving (i.e. a snake of length 4 cannot run into itself).

Implement the SnakeGame class:

SnakeGame(int width, int height, int[][] food) Initializes the object with a screen of size height x width and the positions of the food.
int move(String direction) Returns the score of the game after applying one direction move by the snake. If the game is over, return -1.
 

Example 1:


Input
["SnakeGame", "move", "move", "move", "move", "move", "move"]
[[3, 2, [[1, 2], [0, 1]]], ["R"], ["D"], ["R"], ["U"], ["L"], ["U"]]
Output
[null, 0, 0, 1, 1, 2, -1]

Explanation
SnakeGame snakeGame = new SnakeGame(3, 2, [[1, 2], [0, 1]]);
snakeGame.move("R"); // return 0
snakeGame.move("D"); // return 0
snakeGame.move("R"); // return 1, snake eats the first piece of food. The second piece of food appears at (0, 1).
snakeGame.move("U"); // return 1
snakeGame.move("L"); // return 2, snake eats the second food. No more food appears.
snakeGame.move("U"); // return -1, game over because snake collides with border
 

Constraints:

1 <= width, height <= 104
1 <= food.length <= 50
food[i].length == 2
0 <= ri < height
0 <= ci < width
direction.length == 1
direction is 'U', 'D', 'L', or 'R'.
At most 104 calls will be made to move.

```
class SnakeGame {
int height;
int width;
List<int[]> snake;
int[][] food;
int foodIndex;
int score;
int len=0;
    public SnakeGame(int width, int height, int[][] food) {
        this.width=width;
        this.height=height;
        this.food=food;
     
        this.snake=new ArrayList<>();
        int[] start={0,0};
        this.snake.add(start);
    }
    
    public int move(String direction) {
        int[] l=snake.get(0);
         int[] last={l[0],l[1]};
        if(direction.equalsIgnoreCase("U")){
            last[0]--;
        }else if(direction.equalsIgnoreCase("D")){
            last[0]++;
        }else if(direction.equalsIgnoreCase("L")){
            last[1]--;
        }else if(direction.equalsIgnoreCase("R")){
            last[1]++;
        }
// int[] last={l[0],l[1]};
///within boundary
        if(last[0]==height||last[1]==width||last[0]<0||last[1]<0){
           System.out.println("out of bound");
            return -1;
        }
        //eats itself
        Integer posToNumber=last[0]*width+last[1];
      
         if(eatsSelf(last)){
            return -1;
        }
        //move snake
        snake.add(0,last);
       
        //remove tail if no food
        if(foodIndex<food.length && (food[foodIndex][0]==last[0]&& food[foodIndex][1]==last[1])){
            System.out.println("ate food");
            foodIndex++;
            score++;
            len++; //this is snake length
           
        }
        //snake length should not be greater than food eaten +1 since begining length of snake is 1
          while(snake.size()>len+1){
            snake.remove(snake.size()-1);}
            
        
        
    return score;
    }
    public boolean eatsSelf(int[] po){
        //ignore head by starting from 1
        //for(int i=1;i<snake.size()-1;i++){
            //start from 0 ignore tail
        for(int i=0;i<snake.size()-1;i++){

            int[] s=snake.get(i);
            if(s[0]==po[0] && s[1]==po[1]){
                System.out.println("ate self =true s[0] "+s[0]+" s[1] "+s[1]+" PO {0,1} "+po[0]+" "+po[1]);
                return true;
            }
        }
        return false;
    }
}

/**
 * Your SnakeGame object will be instantiated and called as such:
 * SnakeGame obj = new SnakeGame(width, height, food);
 * int param_1 = obj.move(direction);
 */
```