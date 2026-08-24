import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_reset(dut):
    """Verify reset puts the DUT into its initial state."""

    # Start clock
    cocotb.start_soon(Clock(dut.i_clk, 10, unit="ns").start())

    # Apply reset
    dut.i_rst_n.value = 0
    dut.i_start.value = 0
    dut.i_a.value = 0
    dut.i_b.value = 0

    # Wait for a clock edge while reset is active
    await RisingEdge(dut.i_clk)

    # Release reset
    dut.i_rst_n.value = 1

    # Sum should be zero after reset
    assert dut.o_sum.value.to_unsigned() == 0


@cocotb.test()
async def test_add(dut):
    """Verify that two 8-bit values are added."""

    cocotb.start_soon(Clock(dut.i_clk, 10, unit="ns").start())

    # Reset
    dut.i_rst_n.value = 0
    dut.i_start.value = 0
    dut.i_a.value = 0
    dut.i_b.value = 0

    await RisingEdge(dut.i_clk)

    # Release reset
    dut.i_rst_n.value = 1

    # Put operands on inputs
    dut.i_a.value = 10
    dut.i_b.value = 20

    # IDLE -> RUN
    dut.i_start.value = 1
    await RisingEdge(dut.i_clk)

    # Deassert start
    dut.i_start.value = 0

    # go to IDLE
    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)

    # 10 + 20 = 30
    assert dut.o_sum.value.to_unsigned() == 30
