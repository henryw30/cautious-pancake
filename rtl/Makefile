TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(PWD)/addr_8bit.sv
TOPLEVEL = addr_8bit
COCOTB_TEST_MODULES = test_addr_8bit

SIM = verilator

TRACE ?= 0
ifeq ($(TRACE),1)
    EXTRA_ARGS += --trace --trace-fst --trace-structs
endif

COCOTB_LOG_LEVEL ?= INFO
GPI_LOG_LEVEL ?= INFO
include $(shell cocotb-config --makefiles)/Makefile.sim
