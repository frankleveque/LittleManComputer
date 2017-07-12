/*
    Copyright (C) 2017 Frank Leveque

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    */

#include <iostream>
#include <fstream>
#include <cassert>
#include <iomanip>


std::string prefix = "The little man";

void dies(int inside){
    printf("%.3u - %s %s.\n",inside,prefix.c_str(),"doesn't know what to do with this");
    printf("      %s %s.\n",prefix.c_str(), "dies from stress");
}

int main(int argc, char* argv[]) 
{
    if(argc < 2){
        std::cout << prefix << " needs instructions. Pass in a \"compiled\" instruction file as argument." << std::endl;
        return EXIT_FAILURE;
    } else if(argc >= 2){
        std::cout << "reading " << argv[1] << std::endl;
    } 
    if(argc > 2){
        std::cout << "Ignoring other files" << std::endl;
    }

    std::ifstream file(argv[1]);

    if(!file.good()){
        std::cout << "invalid file: " << argv[1] << std::endl;
        return EXIT_FAILURE;
    } 

    uint32_t accumulator = 0;
    uint8_t programCounter = 0;
    uint32_t mailboxes[100];

    std::string str; 
    int counter = 0;
    while(std::getline(file, str)){
        if(counter < 100){
            if(str == ""){
                printf("Empty line replaced with 0\n");
                str = "0";
            }
            mailboxes[counter] = std::stoi(str);
        }
        else{
            std::cout << "Ignoring extra instructions" << std::endl;
            break;
        }
        ++counter;
    }

    //read value at box
    int inside = mailboxes[programCounter];
    while(true){

        int address = inside % 100;

//INPUT/OUTPUT---------------------------------------------------------------------------------------------
        if(inside >= 900){
            if(address == 1){
                printf("%.3u - %s %s\n",inside,prefix.c_str(),"waits by the inbox for information to fall in...");
                std::string val = ""; 
                while(true){
                    std::cout << "      Enter Value from 0 to 999: ";
                    std::cin >> val;
                    try{
                        int temp = std::stoi(val);
                        if(temp > 999 || temp < 0)
                            continue;
                        printf("      %s %s %u.\n", prefix.c_str(), "changes the working value to", temp); 
                        accumulator = temp;
                        break;
                    }catch(std::exception &e) {
                        continue;
                    }
                }
            }
            else if(address == 2){
                printf("%.3u - %s %s.\n",inside,prefix.c_str(),"puts a copy of the working value in the outbox");
                printf("      %s %i\n", "Outbox: ", accumulator);
            }
            else{
                dies(inside);
                break;      
            }
        }
//BRANCH IF POSITIVE---------------------------------------------------------------------------------------
        else if(inside >= 800){
            printf("%.3u - %s %s\n",inside,prefix.c_str(),"checks if working value is positive...");
            if(accumulator > 0){
                printf("      %s %s %s %u.\n", "It is.", prefix.c_str(), "jumps to mailbox", address); 
                programCounter = address;
                inside = mailboxes[programCounter];
                continue;
            }
            printf("      %s \n", "It's not."); 
        }
//BRANCH IF ZERO-------------------------------------------------------------------------------------------
        else if(inside >= 700){
            printf("%.3u - %s %s\n",inside,prefix.c_str(),"checks if working value is zero...");
            if(accumulator == 0){
                printf("      %s %s %s %u.\n", "It is.", prefix.c_str(), "jumps to mailbox", address); 
                programCounter = address;
                inside = mailboxes[programCounter];
                continue;
            }
            printf("      %s \n", "It's not."); 
        }
//BRANCH UNCONDITIONAL-------------------------------------------------------------------------------------
        else if(inside >= 600){
            printf("%.3u - %s %s %u.\n",inside,prefix.c_str(),"jumps to mailbox", address);
            programCounter = address;
            inside = mailboxes[programCounter];
            continue;
        }
//LOAD-----------------------------------------------------------------------------------------------------
        else if(inside >= 500){
            printf("%.3u - %s %s %u %s.\n",inside,prefix.c_str(),"takes the value in mailbox", address, "and sets it as the working value");
            accumulator = mailboxes[address];
        }
//STORE----------------------------------------------------------------------------------------------------
        else if(inside >= 300 && inside < 400){
            printf("%.3u - %s %s %u.\n",inside,prefix.c_str(),"puts a copy of the working value in mailbox", address);
            mailboxes[address] = accumulator;
        }
//SUBTRACT-------------------------------------------------------------------------------------------------
        else if(inside >= 200){
            printf("%.3u - %s %s %u %s.\n",inside,prefix.c_str(),"subtracts the value in mailbox", address, "from the working value");
            accumulator -= mailboxes[address];
        }
//ADD------------------------------------------------------------------------------------------------------
        else if(inside >= 100){
            printf("%.3u - %s %s %u %s.\n",inside,prefix.c_str(),"adds the value in mailbox", address, "to the working value");
            accumulator += mailboxes[address];
        }
//HALT-----------------------------------------------------------------------------------------------------
        else if(inside == 0){
            printf("%.3u - %s %s.\n",inside,prefix.c_str(),"goes on an indefinite coffee break");
            break;    
        }
//???------------------------------------------------------------------------------------------------------
        else{
            dies(inside); 
            break;    
        }
//---------------------------------------------------------------------------------------------------------
        inside = mailboxes[++programCounter];
    }

    printf("      %s \n","Program Halted");
    return 0;
}
