#include "main.h"
#include "rocketlib.h"


int fwmain(void) {
    while (1) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
        HAL_Delay(200);
        uint8_t data[8] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'};
        can_msg_t msg = {0};
        build_debug_raw_msg(PRIO_LOW, HAL_GetTick(), data, &msg);
    }
}