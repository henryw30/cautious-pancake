// TODO: put this in an actual package file
package sm83_types_pkg;
  typedef enum logic [1:0] {
    PC_HOLD = 2'b00,
    PC_INC  = 2'b01,
    PC_LOAD = 2'b10
  } pc_op_t;
endpackage

module fsm
  import sm83_types_pkg::*;
#(
    parameter integer DATA_WIDTH = 16
) (
    input logic i_clk,
    input logic i_rst_n,

    input logic [DATA_WIDTH-1:0] i_pc,
    output pc_op_t o_pc_op,
    output logic [DATA_WIDTH-1:0] o_pc_load
);

  typedef enum logic [1:0] {
    FSM_FETCH  = 2'b00,
    FSM_DECODE = 2'b01,
    FSM_EXEC   = 2'b10
  } fsm_state_t;
  fsm_state_t current_state, next_state;


  always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (!i_rst_n) begin
      current_state <= FSM_FETCH;
    end else begin
      current_state <= next_state;
    end
  end

  always_comb begin
    next_state = current_state;

    case (current_state)
      FSM_FETCH:  next_state = FSM_DECODE;
      FSM_DECODE: next_state = FSM_EXEC;
      FSM_EXEC:   next_state = FSM_FETCH;

      default: ;
    endcase
  end

  always_comb begin
    o_pc_op   = PC_HOLD;
    o_pc_load = '0;

    case (current_state)
      FSM_FETCH: o_pc_op = PC_INC;

      default: ;
    endcase
  end

endmodule
