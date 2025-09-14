#ifndef HAL_TIMER_MOCK_H
#define HAL_TIMER_MOCK_H

#include "fff.h"
#include <stdint.h>

// mock timer states
typedef enum {
    HAL_TIM_STATE_RESET = 0x00, // timer not initialized
    HAL_TIM_STATE_READY = 0x01, // timer initialized and ready
    HAL_TIM_STATE_BUSY = 0x02, // timer internal process ongoing
    HAL_TIM_STATE_ERROR = 0x03 // timer error state
} HAL_TIM_StateTypeDef;

// mock timer register
typedef struct {
    uint32_t CNT; // timer counter register
    uint32_t CR1; // timer control register 1
} TIM_TypeDef;

// mock timer handle structure
typedef struct {
    TIM_TypeDef *Instance; // timer registers base address
    HAL_TIM_StateTypeDef State; // timer operating state
} TIM_HandleTypeDef;

// mock function declarations
DECLARE_FAKE_VALUE_FUNC(HAL_TIM_StateTypeDef, HAL_TIM_IC_GetState, TIM_HandleTypeDef *);
DECLARE_FAKE_VALUE_FUNC(uint32_t, __HAL_TIM_GET_COUNTER, TIM_HandleTypeDef *);

// timer handle mock
extern TIM_HandleTypeDef htim2;

#endif // HAL_TIMER_MOCK_H
