// BEWARE: output is (intentionally) shifted by one
module GoldCode_HDL (
	output [1:0] R,
	input   clk,
	input   reset
);

reg [17:0] x = 18'b000000000000000001;
reg [17:0] y = 18'b11111111111111111;

wire x_feedback;
wire y_feedback;

wire x_tap;
wire y_tap_a, y_tap_b;

assign x_feedback = x[0] ^ x[7];
assign y_feedback = y[0] ^ y[5] ^ y[7] ^ y[10];

assign x_tap = x[4] ^ x[6] ^ x[15];
assign y_tap_a = y[5] ^ y[6] ^ y[8] ^ y[9] ^ y[10];
assign y_tap_b = y[11] ^ y[12] ^ y[13] ^ y[14] ^ y[15];

always @(posedge clk) begin
	if (reset) 
	begin
		x <= 18'b000000000000000001;
		y <= 18'b111111111111111111;
	end
	else
	begin
		x <= {x_feedback, x[17:1]};
		y <= {y_feedback, y[17:1]};
	end
end

assign R = {x_tap ^ y_tap_a ^ y_tap_b, x[0] ^ y[0]};

endmodule
