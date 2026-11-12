#include "main.h"
#include "stm32h5xx_hal.h"
#include "stm32h5xx_hal_gpio.h"

int fwmain(void) {
    while (1) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
        HAL_Delay(200);
    }
}