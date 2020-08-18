// verilator -Wall --trace -cc GoldCode_HDL.v --exe --build goldcode_test.cpp -CFLAGS --std=c++17

#include <cstdio>
#include "VGoldCode_HDL.h"
#include <verilated.h>
#include <verilated_vcd_c.h>

class GoldCode_Testbench {
	// Need to add a new class variable
	VerilatedVcdC	*m_trace;
	unsigned int m_tickcount;
    VGoldCode_HDL *m_dut;

public:
	GoldCode_Testbench(void) {
		// According to the Verilator spec, you *must* call
		// traceEverOn before calling any of the tracing functions
		// within Verilator.
		Verilated::traceEverOn(true);
		m_tickcount = 0;
        m_dut = new VGoldCode_HDL;
        m_trace = nullptr;
	}

    ~GoldCode_Testbench(void) {
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

    virtual void set_reset(bool rst) {
        m_dut->reset = rst ? 1 : 0;
    }

    virtual void init_tb() {
        set_reset(true);
        tick();
        set_reset(false);
    }

    virtual int next_R() {
        tick();
        return m_dut->R;
    }
};

// ADAPTED FROM GNURADIO GR-DTV


int parity_chk(long a, long b)
{
    int c = 0;
    a = a & b;
    for (int i = 0; i < 18; i++) {
        if (a & (1L << i)) {
            c++;
        }
    }
    return c & 1;
}

void init_xy(int code_idx, long &x, long &y) {
    x = 0x00001;
    y = 0x3FFFF;

    for (int n = 0; n < code_idx; n++) {
        int xb = parity_chk(x, 0x0081);

        x >>= 1;
        if (xb) {
            x |= 0x20000;
        }
    }
}

int next_code(long &x, long &y)
{
    int xa, xb, xc, ya, yb, yc;
    int rn, zna, znb;

    xa = parity_chk(x, 0x8050);
    xb = parity_chk(x, 0x0081);
    xc = x & 1;

    x >>= 1;
    if (xb) {
        x |= 0x20000;
    }

    ya = parity_chk(y, 0x04A1);
    yb = parity_chk(y, 0xFF60);
    yc = y & 1;

    y >>= 1;
    if (ya) {
        y |= 0x20000;
    }

    zna = xc ^ yc;
    znb = xa ^ yb;
    rn = (znb << 1) + zna;
    return rn;
}

const int FRAME_SIZE_NORMAL = 64800;
const int MAX_CLKS = FRAME_SIZE_NORMAL;

int main(int argc, char** argv, char** env) {
    
    Verilated::commandArgs(argc, argv);


    GoldCode_Testbench tb;
    tb.opentrace("goldcode.vcd");
    tb.init_tb();

    long x;
    long y;
    init_xy(0, x, y);

    // Output is shifted by one place
    // Advance reference to match
    next_code(x, y);

    for (int i = 0; i < MAX_CLKS; i++) {
        int expected = next_code(x, y);
        int actual = tb.next_R();
        // printf("%05d: Got %d expected %d\n", i, actual, expected);
        if (actual != expected) {
            printf("%05d: OUTPUT WRONG! \t Got %d expected %d\n", i, actual, expected);
            tb.close();
            exit(1);
        }
        assert(actual == expected);
    }

    printf("Test passed.\n");

    tb.close();
    exit(0);
}
