module addr_8bit #(
    parameter int DATA_WIDTH = 8
) (
    input logic i_clk,
    input logic i_rst_n,
    input logic i_start,
    input logic [DATA_WIDTH-1:0] i_a,
    input logic [DATA_WIDTH-1:0] i_b,

    output logic [DATA_WIDTH-1:0] o_sum
);

  typedef enum logic [1:0] {
    IDLE = 2'b00,
    RUN  = 2'b01,
    DONE = 2'b10
  } state_t;

  state_t current_state, next_state;
  logic [DATA_WIDTH-1:0] sum_, a_, b_;

  always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (!i_rst_n) begin
      sum_ <= 0;
      a_ <= 0;
      b_ <= 0;
      current_state <= IDLE;
    end else begin
      current_state <= next_state;

      case (current_state)
        IDLE: begin
          if (i_start) begin
            a_ <= i_a;
            b_ <= i_b;
          end
        end
        RUN: begin
          sum_ <= a_ + b_;
        end
        default: ;
      endcase
    end
  end

  // next state logic
  always_comb begin
    next_state = current_state;

    case (current_state)
      IDLE: begin
        if (i_start) next_state = RUN;
      end
      RUN: begin
        next_state = DONE;
      end
      DONE: begin
        next_state = IDLE;
      end
      default: next_state = IDLE;
    endcase
  end

  assign o_sum = sum_;

endmodule
