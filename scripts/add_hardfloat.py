# see https://community.platformio.org/t/error-object-uses-vfp-register-arguments-firmware-elf-does-not/25263/2
Import("env")
flags = [
   "-mfloat-abi=hard",
   "-mfpu=fpv5-sp-d16"
]
env.Append(CCFLAGS=flags, LINKFLAGS=flags)

# GCC 12.3.1 segfaults in this file at -O2/-O3. I2C calls HAL_DMAEx_GetFifoLevel from it.
def _dma_ex_no_opt(env, node):
    ccflags = [f for f in env["CCFLAGS"] if not str(f).startswith("-O")]
    return env.Object(node, CCFLAGS=ccflags + ["-O0"])[0]

env.AddBuildMiddleware(_dma_ex_no_opt, "*stm32h5xx_hal_dma_ex.c*")
