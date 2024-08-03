module syn_top
(
    input              clk     ,
    input              rst_n   ,
    input              a_input ,
    input        [7:0] b_input ,
    output logic [7:0] c_output,
    output logic       d_output
);

// parameter
localparam C_XXXX = 32;

// declare
    logic a;
    logic [7:0] b;
    logic [7:0] c;
    logic d;

// input pipe
always_ff@(posedge clk or negedge rst_n)
begin
    if(!rst_n)begin
        a <= '0;
        b <= '0;
    end
    else begin
        a <= a_input;
        b <= b_input;
    end
end

// output pipe
always_ff@(posedge clk or negedge rst_n)
begin
    if(!rst_n)begin
        c_output <= '0;
        d_output <= '0;
    end
    else begin
        c_output <= c;
        d_output <= d;
    end
end

// instance
xxx_top u_xxx_top(
    .a (a),
    .b (b),
    .c (c),
    .d (d)
);

endmodule