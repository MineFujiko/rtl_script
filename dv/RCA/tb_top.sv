`timescale 1ns/1ps

module tb_top();

parameter CLK_PERIOD = 1ns;
bit clk;
bit rstn;

initial begin
    clk=0;
    forever begin
        #(CLK_PERIOD/2) clk = ~clk;
    end
end

initial begin
    rstn = 0;
    #500ns rstn=1;
end

parameter C_WIDTH = 1;

logic  [C_WIDTH-1:0]  din_a                 ;
logic  [C_WIDTH-1:0]  din_b                 ;
logic  [C_WIDTH  :0]  dout                  ;

RCA #(
    .C_WIDTH ( C_WIDTH ))
 u_RCA (
    .din_a                   ( din_a  [C_WIDTH-1:0] ),
    .din_b                   ( din_b  [C_WIDTH-1:0] ),

    .dout                    ( dout   [C_WIDTH  :0] )
);

scoreboard_dut #(
    .C_WIDTH ( C_WIDTH ))
 u_scoreboard_dut (
    .din_a                   ( din_a  [C_WIDTH-1:0] ),
    .din_b                   ( din_b  [C_WIDTH-1:0] ),

    .dout                    ( dout   [C_WIDTH  :0] )
);

`include "tc_dut.sv"

initial begin

    tc_dut();

    # 100ns;
    $display("Simulation is done.");
    $finish;
end

initial begin
    $fsdbDumpfile("tb_top.fsdb");
    $fsdbDumpvars(0,tb_top);
    $fsdbDumpMDA(0,tb_top);
end

endmodule