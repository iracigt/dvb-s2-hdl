// ODD NTAPS
module IQ_FIRFilter (
    input i_clk_x16,
    input i_rst,
    input i_en,
    input [7:0] i_I,
    input [7:0] i_Q,
    output o_ready,
    output o_valid,
    output [15:0] o_I,
    output [15:0] o_Q
);
localparam INITIAL_COEFFS  = "taps.mem";

// 8 bit input
// 16 bit taps
// 31 symmetric taps (16 unique values)
// 16 bit output
// 2 MAC units

reg [15:0] taps [0:15];         // 16 coeffs
reg [7:0] left_mem_i [0:15];    // Block RAM holding i0 - i15
reg [7:0] right_mem_i [0:15];   // Block RAM holding i16 - i31
reg [7:0] left_mem_q [0:15];    // Block RAM holding q0 - q15
reg [7:0] right_mem_q [0:15];   // Block RAM holding q16 - q31

genvar i;
generate // optional if > *-2001
for (i = 0; i < 16 ; i = i + 1) begin 
    initial begin
        left_mem_i[i] = 0;
        right_mem_i[i] = 0;
        left_mem_q[i] = 0;
        right_mem_q[i] = 0;
    end
end
endgenerate

reg [3:0] load_idx = 15;         // Index to load next sample into
                                // Also index of oldest sample

initial $readmemh(INITIAL_COEFFS, taps);

reg [3:0] state_idx = 0;

always @(posedge i_clk_x16) begin
    if (i_rst) begin
        state_idx <= 14; // -2
    end else if (i_en) begin
        state_idx <= state_idx + 1'b1;
    end

    if (state_idx == 15) begin
        load_idx <= load_idx + 1;
        left_mem_i[load_idx+1] <= i_I;
        left_mem_q[load_idx+1] <= i_Q;
        right_mem_i[load_idx+1] <= left_mem_i[load_idx + 1];
        right_mem_q[load_idx+1] <= left_mem_q[load_idx + 1];
    end
end


// Consider delay of 8 in left EBRAM (0 newest, 8 oldest)
// 0 8 7 6 5 4 3 2 1
// ^--- Load index

// Consider delay of 8 in right EBRAM (0 newest, 8 oldest)
// 0 8 7 6 5 4 3 2 1
// ^--- Load index

wire [3:0] cur_left_idx;
wire [3:0] cur_right_idx;
assign cur_left_idx = load_idx - state_idx;
assign cur_right_idx = (load_idx + 2) + state_idx;

wire [7:0] cur_left_samp_i;
wire [7:0] cur_right_samp_i;
wire [7:0] cur_left_samp_q;
wire [7:0] cur_right_samp_q;

assign cur_left_samp_i = left_mem_i[cur_left_idx];
assign cur_right_samp_i = state_idx == 15 ? 8'b0 : right_mem_i[cur_right_idx];
assign cur_left_samp_q = left_mem_q[cur_left_idx];
assign cur_right_samp_q = state_idx == 15 ? 8'b0 : right_mem_q[cur_right_idx];

wire [15:0] sum_a_i;
// wire [15:0] i_sum_b;
wire [15:0] sum_a_q;
// wire [15:0] q_sum_b;

/* verilator lint_off UNUSED */
wire [31:0] acc_a_i;
// wire [31:0] i_acc_b;
wire [31:0] acc_a_q;
// wire [31:0] q_acc_b;
/* verilator lint_on UNUSED */

assign sum_a_i = {8'b0, cur_left_samp_i} + {8'b0, cur_right_samp_i};
assign sum_a_q = {8'b0, cur_left_samp_q} + {8'b0, cur_right_samp_q};


wire [15:0] cur_tap;
assign cur_tap = taps[state_idx];

wire dsp_clr;
assign dsp_clr = state_idx == 0;

wire [31:0] loopback_a_i;
wire [31:0] loopback_a_q;

assign loopback_a_i = dsp_clr ? 32'b0 : acc_a_i;
assign loopback_a_q = dsp_clr ? 32'b0 : acc_a_q;

assign o_I = o_valid ? acc_a_i[23:8] : 16'b0;
assign o_Q = o_valid ? acc_a_q[23:8] : 16'b0;
assign o_valid = state_idx == 0;
assign o_ready = state_idx == 14;

/* verilator lint_off PINMISSING */
SB_MAC16 #(
    .C_REG(0), 
    .A_REG(0), 
    .B_REG(0), 
    .D_REG(0), 
    .TOP_8x8_MULT_REG(0), 
    .BOT_8x8_MULT_REG(0),
    .PIPELINE_16x16_MULT_REG1(0),
    .PIPELINE_16x16_MULT_REG2(0),
    .TOPOUTPUT_SELECT(1),
    .TOPADDSUB_LOWERINPUT(2),
    .TOPADDSUB_UPPERINPUT(1),
    .TOPADDSUB_CARRYSELECT(3),
    .BOTOUTPUT_SELECT(1),
    .BOTADDSUB_LOWERINPUT(2),
    .BOTADDSUB_UPPERINPUT(1),
    .BOTADDSUB_CARRYSELECT(0), 
    .MODE_8x8(0), 
    .A_SIGNED(0), 
    .B_SIGNED(1)
) i_sbmac_a (
    .CLK(i_clk_x16),
    .CE(i_en),
    .A(sum_a_i),
    .B(cur_tap),
    .C(loopback_a_i[31:16]),
    .D(loopback_a_i[15:0]),
    .O(acc_a_i)
);

SB_MAC16 #(
    .C_REG(0), 
    .A_REG(0), 
    .B_REG(0), 
    .D_REG(0), 
    .TOP_8x8_MULT_REG(0), 
    .BOT_8x8_MULT_REG(0),
    .PIPELINE_16x16_MULT_REG1(0),
    .PIPELINE_16x16_MULT_REG2(0),
    .TOPOUTPUT_SELECT(1),
    .TOPADDSUB_LOWERINPUT(2),
    .TOPADDSUB_UPPERINPUT(1),
    .TOPADDSUB_CARRYSELECT(3),
    .BOTOUTPUT_SELECT(1),
    .BOTADDSUB_LOWERINPUT(2),
    .BOTADDSUB_UPPERINPUT(1),
    .BOTADDSUB_CARRYSELECT(0), 
    .MODE_8x8(0), 
    .A_SIGNED(0), 
    .B_SIGNED(1)
    ) q_sbmac_a (
    .CLK(i_clk_x16),
    .CE(i_en),
    .A(sum_a_q),
    .B(cur_tap),
    .C(loopback_a_q[31:16]),
    .D(loopback_a_q[15:0]),
    .O(acc_a_q)
);
/* verilator lint_on PINMISSING */

endmodule
