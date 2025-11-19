#ifndef LSM6DSO_H
#define LSM6DSO_H

#include <stdint.h>

#include "rocketlib/include/common.h"

typedef struct
{
    double x;
    double y;
    double z;
} vector3d_t;

/**
 * @brief Initializes the LSM6DSO incl all register configs
 * @note Must be called after scheduler start
 * @return Status of the operation
 */
w_status_t lsm6dso_init();

/**
 * @brief Retrieves accelerometer data.
 * @param data Pointer to store the converted accelerometer data (gravities)
 */
w_status_t lsm6dso_get_acc_data(vector3d_t *data);

/**
 * @brief Retrieves gyroscope data.
 * @param data Pointer to store the converted gyroscope data (deg/s)
 */
w_status_t lsm6dso_get_gyro_data(vector3d_t *data);

/**
 * @brief Performs a basic sanity check using the WHO_AM_I register.
 * @return W_SUCCESS if device who_am_i matches expected value
 */
w_status_t lsm6dso_check_sanity(void);

#endif // LSM6DSO_H