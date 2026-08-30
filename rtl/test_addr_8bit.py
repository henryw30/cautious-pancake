import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_subtraction_examples(dut):

    async def check(a, b, cin, expected_result, expected_h, expected_c):
        dut.i_a.value = a
        dut.i_b.value = b
        dut.i_carry_in.value = cin
        dut.i_sub.value = 1

        await Timer(1, unit="ns")

        assert int(dut.result.value) == expected_result
        assert int(dut.f_z.value) == int(expected_result == 0)
        assert int(dut.f_n.value) == 1
        assert int(dut.f_h.value) == expected_h
        assert int(dut.f_c.value) == expected_c

    # 5 - 3 = 2
    await check(0x05, 0x03, 0, 0x02, 0, 0)

    # 0x10 - 1 = 0x0F
    # Half borrow, but no full borrow
    await check(0x10, 0x01, 0, 0x0F, 1, 0)

    # 0 - 1 = 0xFF
    # Half borrow and full borrow
    await check(0x00, 0x01, 0, 0xFF, 1, 1)

    # 0x10 - 0 - 1 = 0x0F
    # SBC with carry-in
    await check(0x10, 0x00, 1, 0x0F, 1, 0)

    # 0 - 0 - 1 = 0xFF
    # SBC causes full borrow
    await check(0x00, 0x00, 1, 0xFF, 1, 1)

    # 1 - 1 = 0
    await check(0x01, 0x01, 0, 0x00, 0, 0)


@cocotb.test()
async def test_alu_8bit_exhaustive(dut):
    """
    Exhaustively test:

        ADD: A + B
        ADC: A + B + C
        SUB: A - B
        SBC: A - B - C

    For all 256 x 256 x 2 input combinations.
    """

    for a in range(256):
        for b in range(256):
            for carry_in in range(2):
                # -------------------------------------------------
                # ADD / ADC
                # -------------------------------------------------

                dut.i_a.value = a
                dut.i_b.value = b
                dut.i_carry_in.value = carry_in
                dut.i_sub.value = 0

                await Timer(1, unit="ns")

                full_sum = a + b + carry_in
                expected_result = full_sum & 0xFF
                expected_c = int(full_sum > 0xFF)

                low_sum = (a & 0x0F) + (b & 0x0F) + carry_in
                expected_h = int(low_sum > 0x0F)

                expected_z = int(expected_result == 0)
                expected_n = 0

                assert int(dut.result.value) == expected_result, (
                    f"ADD result failure: "
                    f"A={a:02X} B={b:02X} C={carry_in} "
                    f"expected={expected_result:02X} "
                    f"got={int(dut.result.value):02X}"
                )

                assert int(dut.f_z.value) == expected_z, (
                    f"ADD Z failure: A={a:02X} B={b:02X} C={carry_in}"
                )

                assert int(dut.f_n.value) == expected_n, (
                    f"ADD N failure: A={a:02X} B={b:02X} C={carry_in}"
                )

                assert int(dut.f_h.value) == expected_h, (
                    f"ADD H failure: "
                    f"A={a:02X} B={b:02X} C={carry_in} "
                    f"expected={expected_h} "
                    f"got={int(dut.f_h.value)}"
                )

                assert int(dut.f_c.value) == expected_c, (
                    f"ADD C failure: "
                    f"A={a:02X} B={b:02X} C={carry_in} "
                    f"expected={expected_c} "
                    f"got={int(dut.f_c.value)}"
                )

                # -------------------------------------------------
                # SUB / SBC
                # -------------------------------------------------

                dut.i_sub.value = 1

                await Timer(1, unit="ns")

                full_sub = a - b - carry_in
                expected_result = full_sub & 0xFF

                # SM83 subtraction flags represent BORROW.
                expected_c = int(a < (b + carry_in))
                expected_h = int((a & 0x0F) < ((b & 0x0F) + carry_in))

                expected_z = int(expected_result == 0)
                expected_n = 1

                assert int(dut.result.value) == expected_result, (
                    f"SUB result failure: "
                    f"A={a:02X} B={b:02X} C={carry_in} "
                    f"expected={expected_result:02X} "
                    f"got={int(dut.result.value):02X}"
                )

                assert int(dut.f_z.value) == expected_z, (
                    f"SUB Z failure: A={a:02X} B={b:02X} C={carry_in}"
                )

                assert int(dut.f_n.value) == expected_n, (
                    f"SUB N failure: A={a:02X} B={b:02X} C={carry_in}"
                )

                assert int(dut.f_h.value) == expected_h, (
                    f"SUB H failure: "
                    f"A={a:02X} B={b:02X} C={carry_in} "
                    f"expected={expected_h} "
                    f"got={int(dut.f_h.value)}"
                )

                assert int(dut.f_c.value) == expected_c, (
                    f"SUB C failure: "
                    f"A={a:02X} B={b:02X} C={carry_in} "
                    f"expected={expected_c} "
                    f"got={int(dut.f_c.value)}"
                )

    dut._log.info("All 262144 ADD/ADC/SUB/SBC tests passed!")
