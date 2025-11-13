#include "stm32h7xx_hal.h"
#include "FreeRTOS.h"
#include "task.h"
#include "init.h"
#include "gpio.h"
#include "drivers/gpio/gpio.h"

// add more task handles as needed
TaskHandle_t blinky_task_handle = NULL;

// add task priorities as needed
const uint32_t blinky_task_priority = tskIDLE_PRIORITY + 1;

// example blinky task
static void blinky_task(void *pvParameters)
{
    (void)pvParameters;

    for (;;)
    {
        gpio_toggle(GPIO_PIN_RED_LED, 5);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

// Init all modules and spawn all tasks here
w_status_t system_init(void)
{
    w_status_t status = W_SUCCESS;

    // initialize more modules as needed
    status = gpio_init();

    if (status != W_SUCCESS)
    {
        return status;
    }

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
