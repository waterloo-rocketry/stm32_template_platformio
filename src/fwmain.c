#include "can_message/can.h"
#include "main.h"
#include "rocketlib.h"


int fwmain(void) {
    while (1) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
        HAL_Delay(200);
        can_msg_t msg = {0};
    }
}