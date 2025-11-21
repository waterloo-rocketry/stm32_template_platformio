#include "stm32h7xx_hal.h"
#include "gpio.h"

#include "FreeRTOS.h"
#include "task.h"

#include "application/init/init.h"
#include "application/blinky/blinky.h"
#include "driver/lsm6dso/lsm6dso.h"

// add more task handles as needed
TaskHandle_t blinky_task_handle = NULL;

// add task priorities as needed
const uint32_t blinky_task_priority = tskIDLE_PRIORITY + 1;

// Init all modules and spawn all tasks here
w_status_t system_init(void)
{
    // create more tasks as needed
    BaseType_t tasks_created = xTaskCreate(
        blinky_task,
        "blinky",
        configMINIMAL_STACK_SIZE,
        NULL,
        blinky_task_priority,
        &blinky_task_handle);

    if (tasks_created != pdPASS)
    {
        return W_OVERFLOW;
    }

    return W_SUCCESS;
}
