module logic_8bit #(
    parameter integer DATA_WIDTH = 8
) (
    input logic [DATA_WIDTH-1:0] i_a,
    input logic [DATA_WIDTH-1:0] i_b,
    input logic [1:0] i_sel,

    output logic [DATA_WIDTH-1:0] result,
    output logic f_z,
    output logic f_n,
    output logic f_h,
    output logic f_c
);
  typedef enum logic [1:0] {
    OP_AND = 2'b00,
    OP_OR  = 2'b01,
    OP_XOR = 2'b10,
    OP_CPL = 2'b11
  } logic_op_t;

  always_comb begin
    case (i_sel)
      OP_AND: begin
        result = i_a & i_b;

        f_n = '0;
        f_h = '1;
        f_c = '0;
        f_z = (result == '0);
      end
      OP_OR: begin
        result = i_a | i_b;

        f_n = '0;
        f_h = '0;
        f_c = '0;
        f_z = (result == '0);
      end
      OP_XOR: begin
        result = i_a ^ i_b;

        f_n = '0;
        f_h = '0;
        f_c = '0;
        f_z = (result == '0);
      end
      OP_CPL: begin
        result = ~i_a;

        // f_c and f_z do not get set for CPL
        f_z = '0;
        f_n = '1;
        f_h = '1;
        f_c = '0;
      end

      default: ;
    endcase

  end

endmodule
