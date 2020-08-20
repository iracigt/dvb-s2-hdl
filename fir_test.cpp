// verilator -Wall --trace -cc IQ_FIRFilter.v --exe --build fir_test.cpp -CFLAGS --std=c++17

#include <cstdio>
#include "VIQ_FIRFilter.h"
#include <verilated.h>
#include <verilated_vcd_c.h>

class FIR_Testbench {
	// Need to add a new class variable
	VerilatedVcdC	*m_trace;
	unsigned int m_tickcount;
    VIQ_FIRFilter *m_dut;

public:
	FIR_Testbench(void) {
		// According to the Verilator spec, you *must* call
		// traceEverOn before calling any of the tracing functions
		// within Verilator.
		Verilated::traceEverOn(true);
		m_tickcount = 0;
        m_dut = new VIQ_FIRFilter;
        m_trace = nullptr;
	}

    ~FIR_Testbench(void) {
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
		m_dut->i_clk_x16 = 0;
		m_dut->eval();

		//
		// Here's the new item:
		//
		//	Dump values to our trace file
		//
		if (m_trace) m_trace->dump(10*m_tickcount-2);

		// Repeat for the positive edge of the clock
		m_dut->i_clk_x16 = 1;
		m_dut->eval();
		if(m_trace) m_trace->dump(10*m_tickcount);

		// Now the negative edge
		m_dut->i_clk_x16 = 0;
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
        m_dut->i_rst = rst ? 1 : 0;
    }

    virtual void set_enable(bool en) {
        m_dut->i_en = en ? 1 : 0;
    }

    virtual void init_tb() {
        set_enable(true);
        set_reset(true);
        tick();
        set_reset(false);

    }

    virtual bool is_ready() {
        return m_dut->o_ready;
    }

    virtual bool is_valid() {
        return m_dut->o_valid;
    }

    virtual void getIQ(uint16_t &I, uint16_t &Q) {
        I = m_dut->o_I;
        Q = m_dut->o_Q;
    }

    virtual void set_data(uint16_t I, uint16_t Q) {
        m_dut->i_I = I;
        m_dut->i_Q = Q;
    }
};

const int NTAPS = 32;
const int OVERCLK = 16;
const int MAX_CLKS = 694080 * OVERCLK;
// const int MAX_CLKS = 33 * OVERCLK;

int main(int argc, char** argv, char** env) {
    
    Verilated::commandArgs(argc, argv);


    FIR_Testbench tb;
    // tb.opentrace("FIR.vcd");
    tb.init_tb();

    FILE *infile = fopen("fir_in_u8.bin", "rb");
    FILE *outfile = fopen("fir_out_s16.bin", "wb");

    int byte_count = 0;

    for (int i = 0; i < MAX_CLKS; i++) {
        if (tb.is_ready()) {
            uint8_t iq[2] = {0, 0};
            // if (tb.tick_count() < 8) {
            //     iq[0] = 1;
            //     iq[1] = 1;
            // }
            fread(iq, sizeof(uint8_t), 2, infile);
            tb.set_data(iq[0], iq[1]);
            printf("%03d: I = 0x%02X, Q = 0x%02X\n", tb.tick_count(), iq[0], iq[1]);
        }

        tb.tick();

        if (tb.is_valid()) {
            uint16_t iq[2];
            tb.getIQ(iq[0], iq[1]);
            fwrite(iq, sizeof(uint16_t), 2, outfile);
        }
    }

    fclose(infile);
    fclose(outfile);

    //printf("Test finished.\n");

    tb.close();
    exit(0);
}
