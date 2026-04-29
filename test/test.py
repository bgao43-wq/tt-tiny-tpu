import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


async def set_spi(dut, cs_n, sclk, mosi):
    # ui_in[0] = SCLK
    # ui_in[1] = MOSI
    # ui_in[2] = CS_N
    dut.ui_in.value = (cs_n << 2) | (mosi << 1) | sclk


@cocotb.test()
async def test_tiny_tpu_smoke(dut):
    dut._log.info("Start Tiny TPU smoke test")

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.ena.value = 1
    dut.uio_in.value = 0

    # SPI idle: CS_N high, SCLK low, MOSI low
    await set_spi(dut, 1, 0, 0)

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    # Toggle a simple SPI-like bit
    await set_spi(dut, 0, 0, 1)
    await ClockCycles(dut.clk, 5)
    await set_spi(dut, 0, 1, 1)
    await ClockCycles(dut.clk, 5)
    await set_spi(dut, 1, 0, 0)
    await ClockCycles(dut.clk, 10)

    dut._log.info(f"uo_out = {dut.uo_out.value}")

    # Smoke test only: if simulation reaches here, wrapper/test setup is alive.
    assert True