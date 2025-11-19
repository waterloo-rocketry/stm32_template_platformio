#include "driver/lsm6dso/lsm6dso.h"
#include "driver/lsm6dso/LSM6DSO_regmap.h"

#include "i2c.h"
#include "gpio.h"

// LSM6DSO device address
#define LSM6DSO_ADDR 0x6B // we set addr select pin HIGH

// LSM6DSO range
#define LSM6DSO_ACC_RANGE 16.0    // g
#define LSM6DSO_GYRO_RANGE 2000.0 // dps

// LSM6DSO conversion factors
static const double ACC_FS = LSM6DSO_ACC_RANGE / INT16_MAX;   // g / LSB
static const double GYRO_FS = LSM6DSO_GYRO_RANGE / INT16_MAX; // dps / LSB

// Helper function for writing 1 byte via i2c to this addr
static w_status_t write_1_byte(uint8_t addr, uint8_t reg, uint8_t data)
{
    extern I2C_HandleTypeDef hi2c4;
    if (HAL_I2C_Mem_Write(&hi2c4, (addr << 1), reg, I2C_MEMADD_SIZE_8BIT, &data, 1, 100) == HAL_OK)
    {
        return W_SUCCESS;
    }
    else
    {
        return W_FAILURE;
    }
}

/**
 * @brief Initializes the LSM6DSO incl all register configs
 * @note Must be called after scheduler start
 * @return Status of the operation
 */
w_status_t lsm6dso_init()
{
    w_status_t status = W_SUCCESS;

    // Drive addr sel pin HIGH to use each device's "default" i2c addr
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_0, GPIO_PIN_SET);

    // LSM6DSO: https://www.st.com/resource/en/datasheet/lsm6dso.pdf

    // Accel ODR: 208 Hz
    // Accel Fs: max  (+-16g)
    // LPF2_XL_EN: disable 2nd lowpass stage
    // Note: need to set XL_FS_MODE = 0
    status |= write_1_byte(LSM6DSO_ADDR, CTRL1_XL, 0x54);

    // Gyro ODR: 208 Hz
    // Gyro Fs: max (+-2000 dps)
    status |= write_1_byte(LSM6DSO_ADDR, CTRL2_G, 0x5C);

    // BDU Enable
    status |= write_1_byte(LSM6DSO_ADDR, CTRL3_C, 0x44);

    // Gyro LPF1 Bw: 67 Hz
    status |= write_1_byte(LSM6DSO_ADDR, CTRL6_C, 0x00);

    // XL_FS_MODE = 0
    // Accel Lowpass Bandwidth = ODR/2 = 104 Hz
    status |= write_1_byte(LSM6DSO_ADDR, CTRL8_XL, 0x0);

    // Set bit 1 to 1 when not using I3C, recommended by datasheet
    status |= write_1_byte(LSM6DSO_ADDR, CTRL9_XL, 0x02);

    if (status != W_SUCCESS)
    {
        // log error
    }

    return status;
}

/**
 * @brief Performs a basic sanity check using the WHO_AM_I register.
 * @return Status of the operation.
 */
w_status_t lsm6dso_check_sanity(void)
{
    // datasheet: this is the expected value that should be read from WHO_AM_I register
    const uint8_t expected_lsm6dso = 0x6C;
    w_status_t i2c_status = W_SUCCESS;
    w_status_t device_status = W_SUCCESS;
    uint8_t who_am_i_result = 0;
    uint32_t num_bytes = 1; // who_am_i register has 1 byte of data

    // read 1 byte from the who_am_i register
    if (HAL_I2C_Mem_Read(&hi2c4, (LSM6DSO_ADDR << 1), WHO_AM_I_REG, I2C_MEMADD_SIZE_8BIT, &who_am_i_result, num_bytes, 100) != HAL_OK)
    {
        i2c_status |= W_FAILURE;
    }

    // compare the who_am_i reading to the expected value
    if (expected_lsm6dso != who_am_i_result)
    {
        device_status |= W_FAILURE;
    }

    if ((i2c_status != W_SUCCESS) || (device_status != W_SUCCESS))
    {
        return W_FAILURE;
    }

    return W_SUCCESS;
}

/**
 * @brief Retrieves accelerometer data.
 * @return Accelerometer data (gravities)
 */
w_status_t lsm6dso_get_acc_data(vector3d_t *data)
{
    w_status_t status = W_SUCCESS;
    uint8_t raw_bytes[6] = {0};
    uint32_t num_bytes = 6;

    // read 6 bytes from the accelerometer data registers
    if (HAL_I2C_Mem_Read(&hi2c4, (LSM6DSO_ADDR << 1), OUTX_L_A, I2C_MEMADD_SIZE_8BIT, raw_bytes, num_bytes, 100) != HAL_OK)
    {
        status = W_FAILURE;
    }

    if (W_SUCCESS == status)
    {
        // arrange the 6 raw bytes into actual numbers for accelerometer x, y, z
        int16_t raw_x = (int16_t)(((uint16_t)raw_bytes[1] << 8) | raw_bytes[0]);
        int16_t raw_y = (int16_t)(((uint16_t)raw_bytes[3] << 8) | raw_bytes[2]);
        int16_t raw_z = (int16_t)(((uint16_t)raw_bytes[5] << 8) | raw_bytes[4]);

        // convert from unitless values into unit of gravities
        data->x = raw_x * ACC_FS;
        data->y = raw_y * ACC_FS;
        data->z = raw_z * ACC_FS;
    }
    return status;
}

/**
 * @brief Retrieves gyroscope data.
 * @return Gyroscope data (deg/s)
 */
w_status_t lsm6dso_get_gyro_data(vector3d_t *data)
{
    uint8_t raw_bytes[6] = {0};
    w_status_t status = W_SUCCESS;
    uint32_t num_bytes = 6;

    if (HAL_I2C_Mem_Read(&hi2c4, (LSM6DSO_ADDR << 1), OUTX_L_G, I2C_MEMADD_SIZE_8BIT, raw_bytes, num_bytes, 100) != HAL_OK)
    {
        status = W_FAILURE;
    }

    if (W_SUCCESS == status)
    {
        int16_t gx = (int16_t)(((uint16_t)raw_bytes[1] << 8) | raw_bytes[0]);
        int16_t gy = (int16_t)(((uint16_t)raw_bytes[3] << 8) | raw_bytes[2]);
        int16_t gz = (int16_t)(((uint16_t)raw_bytes[5] << 8) | raw_bytes[4]);
        data->x = gx * GYRO_FS;
        data->y = gy * GYRO_FS;
        data->z = gz * GYRO_FS;
    }
    return status;
}
