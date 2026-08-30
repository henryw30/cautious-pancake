module addr_8bit #(
    parameter int DATA_WIDTH = 8
) (
    input logic [DATA_WIDTH-1:0] i_a,
    input logic [DATA_WIDTH-1:0] i_b,
    input logic i_carry_in,
    input logic i_sub,

    output logic [DATA_WIDTH-1:0] result,
    output logic f_z,
    output logic f_n,
    output logic f_h,
    output logic f_c
);
  logic [DATA_WIDTH:0] full_sum;
  logic [         4:0] half_sum;
  logic [         4:0] b_low_with_carry;
  logic [DATA_WIDTH:0] b_with_carry;

  always_comb begin
    result           = '0;
    f_z              = 1'b0;
    f_n              = i_sub;
    f_h              = 1'b0;
    f_c              = 1'b0;
    full_sum         = '0;
    half_sum         = '0;
    b_low_with_carry = '0;
    b_with_carry     = '0;

    if (i_sub) begin
      // SUB/SBC
      full_sum         = {1'b0, i_a} + {1'b0, ~i_b} + (9'd1 - {8'd0, i_carry_in});
      result           = full_sum[DATA_WIDTH-1:0];

      // carry flags
      b_low_with_carry = {1'b0, i_b[3:0]} + {4'd0, i_carry_in};
      b_with_carry     = {1'b0, i_b} + {8'd0, i_carry_in};

      f_h              = {1'b0, i_a[3:0]} < b_low_with_carry;
      f_c              = {1'b0, i_a} < b_with_carry;
    end else begin
      // ADD/ADC
      full_sum = {1'b0, i_a} + {1'b0, i_b} + {8'd0, i_carry_in};
      result = full_sum[DATA_WIDTH-1:0];
      half_sum = {1'b0, i_a[3:0]} + {1'b0, i_b[3:0]} + {4'd0 + i_carry_in};

      // carry flags
      f_h = half_sum[4];
      f_c = full_sum[DATA_WIDTH];
    end

    f_z = (result == '0);
  end

endmodule
