from controller import MouseController
import time

def main():
    controller = MouseController()

    controller.begin()

    while(1):
        controller.run()
        
    # for state in controller.states:
    #     controller.transitionTo(state)
    #     time.sleep(1)
    #     controller.run()
    #     time.sleep(1)
    
if __name__ == '__main__':
    main()