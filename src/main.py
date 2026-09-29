from controller import MouseController
from CLI import CommandInterface
import time



def main():
    controller = MouseController()
    cli = CommandInterface(controller)

    controller.begin()
    cli.begin()
    
    while(1):
        cli.run()
        controller.run()

        
    
if __name__ == '__main__':
    main()