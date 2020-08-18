
module SymbolShifter (
	output  irq,
	output [2:0] sym,
	input   clk,
	input  [7:0] data,
	input   hold,
	input   reset
);
    
   reg [2:0] state;
   reg [9:0] shift_reg;
   reg req; 
 
    always @(posedge clk)
    begin
        if (reset) begin
            state <= 3; // -1
            shift_reg <= 10'b1111111111;
            req <= 0;
        end else if (hold) begin    
            // pass
            req <= 0;
        end else begin
            case (state)
                0 : shift_reg <= {2'b0, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]};
                //0 : shift_reg <= {2'b0, data[7:0]};
                1 : shift_reg <= {1'b0, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], shift_reg[3]};
                //1 : shift_reg <= {1'b0, data[7:0], shift_reg[3]};
                2 : shift_reg <= {data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], shift_reg[4:3]};
                //2 : shift_reg <= {data[7:0], shift_reg[4:3]};
                default : shift_reg <= {3'b0, shift_reg[9:3]} ;
            endcase
            
            case (state)
                0 : state <= 5;
                1 : state <= 6;
                2 : state <= 7;
                3 : state <= 0;
                4 : state <= 1;
                5 : state <= 2;
                6 : state <= 3;
                7 : state <= 4;
            endcase

            req <= (state == 3) || (state == 4) || (state == 5); // next state < 3
        end
    end 
    //assign sym[2:0] = pass ? data[2:0] : shift_reg[2:0];
    // 
    assign sym[2:0] = {shift_reg[0], shift_reg[1], shift_reg[2]};
    assign irq = req;

endmodule
