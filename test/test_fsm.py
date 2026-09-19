import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb_tools.runner import get_runner

proj_path = Path(__file__).resolve().parent
rtl_path = proj_path.parent / "rtl"
build_dir = proj_path.parent / "build" / "fsm"


def test_fsm_runner():
    sim = os.getenv("SIM", "verilator")
    runner = get_runner(sim)
    runner.build(
        sources=[rtl_path / "fsm.sv"],
        hdl_toplevel="fsm",
        build_dir=build_dir,
        build_args=[
            "--trace-fst",
            "--trace-structs",
        ],
        always=True,
        waves=True,
    )
    runner.test(hdl_toplevel="fsm", test_module="test_fsm", waves=True)


@cocotb.test()
async def test_fsm_smoke(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, unit="ns").start())

    dut.i_rst_n.value = 0
    dut.i_pc.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_rst_n.value = 1

    for i in range(10):
        await RisingEdge(dut.i_clk)
