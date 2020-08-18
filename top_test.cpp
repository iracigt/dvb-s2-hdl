// verilator -Wall --trace -cc top.v --exe --build top_test.cpp -CFLAGS --std=c++17

#include <cstdio>
#include "Vtop.h"
#include <verilated.h>
#include <verilated_vcd_c.h>

class Top_Testbench {
	// Need to add a new class variable
	VerilatedVcdC	*m_trace;
	unsigned int m_tickcount;
    Vtop *m_dut;

public:
	Top_Testbench(void) {
		// According to the Verilator spec, you *must* call
		// traceEverOn before calling any of the tracing functions
		// within Verilator.
		Verilated::traceEverOn(true);
		m_tickcount = 0;
        m_dut = new Vtop;
        m_trace = nullptr;
	}

    ~Top_Testbench(void) {
        delete m_dut;
    }

	// Open/create a trace file
	virtual void opentrace(const char *vcdname) {
		if (!m_trace) {
			m_trace = new VerilatedVcdC;
			m_dut->trace(m_trace, 99);
			m_trace->open(vcdname);
		}
	}

	// Close a trace file
	virtual void close(void) {
		if (m_trace) {
			m_trace->close();
			m_trace = NULL;
		}
	}

	virtual void tick(void) {
		// Make sure the tickcount is greater than zero before
		// we do this
		m_tickcount++;

		// Allow any combinatorial logic to settle before we tick
		// the clock.  This becomes necessary in the case where
		// we may have modified or adjusted the inputs prior to
		// coming into here, since we need all combinatorial logic
		// to be settled before we call for a clock tick.
		//
		m_dut->clk = 0;
		m_dut->eval();

		//
		// Here's the new item:
		//
		//	Dump values to our trace file
		//
		if (m_trace) m_trace->dump(10*m_tickcount-2);

		// Repeat for the positive edge of the clock
		m_dut->clk = 1;
		m_dut->eval();
		if(m_trace) m_trace->dump(10*m_tickcount);

		// Now the negative edge
		m_dut->clk = 0;
		m_dut->eval();
		if (m_trace) {
			// This portion, though, is a touch different.
			// After dumping our values as they exist on the
			// negative clock edge ...
			m_trace->dump(10*m_tickcount+5);
			//
			// We'll also need to make sure we flush any I/O to
			// the trace file, so that we can use the assert()
			// function between now and the next tick if we want to.
			m_trace->flush();
		}
	}

    virtual int tick_count() {
        return m_tickcount;
    }

    virtual void set_reset(bool rst) {
        m_dut->rst = rst ? 1 : 0;
    }

    virtual void init_tb() {
        set_reset(true);
        tick();
        set_reset(false);
    }

    virtual bool is_ready() {
        return m_dut->next_data;
    }

    virtual bool is_valid() {
        return m_dut->valid;
    }

    virtual void getIQ(uint16_t &I, uint16_t &Q) {
        I = m_dut->I;
        Q = m_dut->Q;
    }

    virtual void set_data(char b) {
        m_dut->data = b;
    }
};

const int FRAME_SIZE_NORMAL = 64800;
// const int MAX_CLKS = 8 * 16 * (FRAME_SIZE_NORMAL / 3 + 90);
// const int MAX_CLKS = 128 * 2 * 16 * (FRAME_SIZE_NORMAL / 3 + 90);
// onst int MAX_CLKS = 2 * 16 * 200;

const int MAX_CLKS = 64 * 2 * 16 * (FRAME_SIZE_NORMAL / 3 + 90);

int main(int argc, char** argv, char** env) {
    
    Verilated::commandArgs(argc, argv);


    Top_Testbench tb;
    //tb.opentrace("top.vcd");
    tb.init_tb();

    FILE *infile = fopen("pkt.bin", "rb");
    FILE *outfile = fopen("iq_bytes.bin", "wb");

    int byte_count = 0;

    char pkt[8100] = {0};
    fread(pkt, sizeof(char), 81000, infile);


    for (int i = 0; i < MAX_CLKS; i++) {
        if (tb.is_ready()) {
            tb.set_data(pkt[byte_count % 8100]);
            printf("%03.01f%%: byte %d\n", 100.0 * i / MAX_CLKS, byte_count++);
        }

        tb.tick();

        if (tb.is_valid()) {
            uint16_t iq[2];
            tb.getIQ(iq[0], iq[1]);
            fwrite(iq, sizeof(short), 2, outfile);
        }
    }

    fclose(infile);
    fclose(outfile);

    //printf("Test finished.\n");

    tb.close();
    exit(0);
}
